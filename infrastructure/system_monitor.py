"""
PRODUCTION HEALTH MONITORING
System health checks, metrics collection, and performance monitoring
"""
import psutil
import threading
import time
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

from config_production import MONITORING_CONFIG
from infrastructure.production_logger import get_production_logger


@dataclass
class HealthStatus:
    """Health status snapshot."""
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    memory_mb: float
    gpu_memory_mb: Optional[float]
    gpu_utilization: Optional[float]
    active_threads: int
    status: str  # healthy, warning, critical


class SystemHealthMonitor:
    """Monitor system health and performance metrics."""
    
    def __init__(self):
        self.logger = get_production_logger().get_logger("health")
        self.monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.last_status: Optional[HealthStatus] = None
        self.metrics_history: list = []
        self.max_history = 1000
        
        # Thresholds
        self.cpu_warning_threshold = 80
        self.cpu_critical_threshold = 95
        self.memory_warning_threshold = 80
        self.memory_critical_threshold = 95
    
    def start(self):
        """Start health monitoring."""
        if self.monitoring:
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop,
            daemon=True,
            name="HealthMonitor"
        )
        self.monitor_thread.start()
        self.logger.debug("Health monitoring started")
    
    def stop(self):
        """Stop health monitoring."""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        self.logger.debug("Health monitoring stopped")
    
    def _monitor_loop(self):
        """Continuous monitoring loop."""
        while self.monitoring:
            try:
                self.last_status = self._get_status()
                self._check_thresholds(self.last_status)
                self.metrics_history.append(self.last_status)
                
                # Limit history
                if len(self.metrics_history) > self.max_history:
                    self.metrics_history.pop(0)
                
                time.sleep(MONITORING_CONFIG["metrics_update_interval"])
            except Exception as e:
                self.logger.log_error(f"Monitoring error: {e}", exc_info=True)
    
    def _get_status(self) -> HealthStatus:
        """Get current system status."""
        # CPU and Memory
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        
        # GPU (if available)
        gpu_memory_mb = None
        gpu_utilization = None
        try:
            import torch
            if torch.cuda.is_available():
                gpu_memory_mb = torch.cuda.memory_allocated() / 1024 / 1024
                gpu_utilization = torch.cuda.utilization() if hasattr(torch.cuda, 'utilization') else None
        except:
            pass
        
        # Determine status
        status = self._determine_status(cpu_percent, memory.percent)
        
        return HealthStatus(
            timestamp=datetime.now(),
            cpu_percent=cpu_percent,
            memory_percent=memory.percent,
            memory_mb=memory.used / 1024 / 1024,
            gpu_memory_mb=gpu_memory_mb,
            gpu_utilization=gpu_utilization,
            active_threads=threading.active_count(),
            status=status
        )
    
    def _determine_status(self, cpu: float, memory: float) -> str:
        """Determine overall health status."""
        if (cpu > self.cpu_critical_threshold or 
            memory > self.memory_critical_threshold):
            return "critical"
        elif (cpu > self.cpu_warning_threshold or 
              memory > self.memory_warning_threshold):
            return "warning"
        return "healthy"
    
    def _check_thresholds(self, status: HealthStatus):
        """Check and alert on threshold violations."""
        if status.status == "critical":
            self.logger.log_warning(
                f"CRITICAL: CPU={status.cpu_percent:.1f}%, MEM={status.memory_percent:.1f}%"
            )
        elif status.status == "warning":
            self.logger.log_warning(
                f"WARNING: CPU={status.cpu_percent:.1f}%, MEM={status.memory_percent:.1f}%"
            )
    
    def get_status(self) -> Optional[HealthStatus]:
        """Get latest status without waiting."""
        return self.last_status
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics."""
        if not self.last_status:
            return {}
        
        status = self.last_status
        return {
            "timestamp": status.timestamp.isoformat(),
            "cpu_percent": status.cpu_percent,
            "memory_percent": status.memory_percent,
            "memory_mb": status.memory_mb,
            "gpu_memory_mb": status.gpu_memory_mb,
            "gpu_utilization": status.gpu_utilization,
            "active_threads": status.active_threads,
            "status": status.status,
        }
    
    def get_history(self, limit: int = 100) -> list:
        """Get metrics history."""
        return [
            {
                "timestamp": s.timestamp.isoformat(),
                "cpu_percent": s.cpu_percent,
                "memory_percent": s.memory_percent,
                "memory_mb": s.memory_mb,
            }
            for s in self.metrics_history[-limit:]
        ]


class PerformanceTracker:
    """Track performance metrics for components."""
    
    def __init__(self):
        self.logger = get_production_logger().get_logger("performance")
        self.timings: Dict[str, list] = {}
    
    def record_timing(self, component: str, duration_ms: float):
        """Record component timing."""
        if component not in self.timings:
            self.timings[component] = []
        
        self.timings[component].append(duration_ms)
        
        # Keep only recent measurements
        if len(self.timings[component]) > 1000:
            self.timings[component] = self.timings[component][-500:]
    
    def get_stats(self, component: str) -> Dict[str, float]:
        """Get timing statistics for component."""
        if component not in self.timings or not self.timings[component]:
            return {}
        
        timings = self.timings[component]
        return {
            "count": len(timings),
            "avg_ms": sum(timings) / len(timings),
            "min_ms": min(timings),
            "max_ms": max(timings),
            "p95_ms": sorted(timings)[int(len(timings) * 0.95)],
            "p99_ms": sorted(timings)[int(len(timings) * 0.99)] if len(timings) > 100 else None,
        }
    
    def log_stats(self):
        """Log all timing statistics."""
        for component in self.timings:
            stats = self.get_stats(component)
            if stats:
                self.logger.log_metrics({
                    "component": component,
                    **stats
                })


class ResourceCleaner:
    """Manage resource cleanup and optimization."""
    
    def __init__(self):
        self.logger = get_production_logger().get_logger("cleanup")
    
    def cleanup_torch_cache(self):
        """Clean up PyTorch GPU cache."""
        try:
            import torch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                torch.cuda.synchronize()
                self.logger.log_debug("PyTorch cache cleaned")
        except Exception as e:
            self.logger.log_debug(f"PyTorch cleanup skipped: {e}")
    
    def optimize_memory(self):
        """Optimize process memory usage."""
        import gc
        gc.collect()
        self.logger.log_debug("Memory optimization triggered")
    
    def cleanup_all(self):
        """Full cleanup routine."""
        self.cleanup_torch_cache()
        self.optimize_memory()


# Global instances
_health_monitor: Optional[SystemHealthMonitor] = None
_performance_tracker: Optional[PerformanceTracker] = None
_resource_cleaner: Optional[ResourceCleaner] = None


def get_health_monitor() -> SystemHealthMonitor:
    """Get or create health monitor."""
    global _health_monitor
    if _health_monitor is None:
        _health_monitor = SystemHealthMonitor()
    return _health_monitor


def get_performance_tracker() -> PerformanceTracker:
    """Get or create performance tracker."""
    global _performance_tracker
    if _performance_tracker is None:
        _performance_tracker = PerformanceTracker()
    return _performance_tracker


def get_resource_cleaner() -> ResourceCleaner:
    """Get or create resource cleaner."""
    global _resource_cleaner
    if _resource_cleaner is None:
        _resource_cleaner = ResourceCleaner()
    return _resource_cleaner
