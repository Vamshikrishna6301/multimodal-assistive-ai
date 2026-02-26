#!/usr/bin/env python3
"""
GPU-Optimized Multimodal Voice Assistant
Production entry point with CUDA support, comprehensive logging, monitoring, and error handling
"""
import os
import sys
import signal
from datetime import datetime

# ============================================================
# CUDA/GPU CONFIGURATION (MUST BE BEFORE PyTorch IMPORT)
# ============================================================

# Add PyTorch CUDA libraries to PATH
torch_lib_path = r"c:\Users\ramsa\OneDrive\Desktop\multimodal-assistive-ai\.venv-1\Lib\site-packages\torch\lib"
os.environ["PATH"] = f"{torch_lib_path};{os.environ.get('PATH', '')}"

# Set optimization flags
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"  # GPU 0 only

# ============================================================
# PRODUCTION INFRASTRUCTURE INITIALIZATION
# ============================================================

from config_production import (
    get_config, create_directories, AUDIO_CONFIG, 
    VISION_CONFIG, COMPUTE_CONFIG, MONITORING_CONFIG
)
from infrastructure.production_logger import get_production_logger
from infrastructure.system_monitor import (
    get_health_monitor, get_performance_tracker, get_resource_cleaner
)
from infrastructure.error_handling import get_error_handler, retry_with_backoff, RetryConfig

# ============================================================
# APPLICATION IMPORTS
# ============================================================

from voice.voice_loop import VoiceLoop

# Initialize production infrastructure
_logger = None
_health_monitor = None
_performance_tracker = None
_resource_cleaner = None
_error_handler = None


def initialize_production_infrastructure():
    """Initialize all production systems before app startup"""
    global _logger, _health_monitor, _performance_tracker, _resource_cleaner, _error_handler
    
    print("\n" + "=" * 70)
    print("🚀 GPU-OPTIMIZED MULTIMODAL VOICE ASSISTANT (PRODUCTION)")
    print("=" * 70 + "\n")
    
    # 1. Create necessary directories
    print("📁 Creating directory structure...")
    create_directories()
    
    # 2. Initialize logger
    print("📝 Initializing structured logging...")
    _logger = get_production_logger()
    app_logger = _logger.get_logger("main")
    app_logger.info("Application startup initiated")
    
    # 3. Initialize error handler
    print("🛡️  Initializing error handling...")
    _error_handler = get_error_handler()
    
    # 4. Initialize health monitor
    print("💚 Initializing system health monitoring...")
    _health_monitor = get_health_monitor()
    _health_monitor.start()
    
    # 5. Initialize performance tracker
    print("⚡ Initializing performance tracking...")
    _performance_tracker = get_performance_tracker()
    
    # 6. Initialize resource cleaner
    print("🧹 Initializing resource management...")
    _resource_cleaner = get_resource_cleaner()
    
    print()
    return app_logger


@retry_with_backoff(RetryConfig(max_attempts=3, initial_delay=1.0))
def verify_system_ready():
    """Verify CUDA and system configuration with retry logic"""
    import torch
    
    cuda_available = torch.cuda.is_available()
    
    print(f"📊 System Configuration:")
    print(f"   GPU Available: {'✅ Yes' if cuda_available else '❌ No'}")
    
    if cuda_available:
        device_name = torch.cuda.get_device_name(0)
        cuda_version = torch.version.cuda
        pytorch_version = torch.__version__
        
        print(f"   GPU Device: {device_name}")
        print(f"   CUDA Version: {cuda_version}")
        print(f"   PyTorch Version: {pytorch_version}")
        
        # Log GPU configuration
        _logger.get_logger("main").info(
            "GPU configuration verified",
            gpu_device=device_name,
            cuda_version=cuda_version,
            pytorch_version=pytorch_version
        )
    else:
        print("   ⚠️  CUDA not detected. GPU operations may fail.")
        _logger.get_logger("main").warning("CUDA not available, falling back to CPU")
    
    print()
    return cuda_available


def cleanup_on_shutdown():
    """Clean shutdown of all production systems"""
    print("\n🛑 Shutting down application...\n")
    
    app_logger = _logger.get_logger("main") if _logger else None
    
    try:
        if _resource_cleaner:
            print("🧹 Cleaning up resources...")
            _resource_cleaner.cleanup()
        
        if _health_monitor:
            print("💚 Stopping health monitor...")
            _health_monitor.stop()
        
        if _performance_tracker:
            print("📊 Saving performance metrics...")
            metrics = _performance_tracker.get_summary()
            if app_logger:
                app_logger.log_metrics("shutdown", metrics)
        
        if app_logger:
            app_logger.info("Application shutdown complete")
            print("\n✅ All systems shut down gracefully")
        
    except Exception as e:
        if app_logger:
            app_logger.log_error("Shutdown error", {"error": str(e)})
        print(f"\n⚠️  Error during shutdown: {e}")


def handle_signal(signum, frame):
    """Handle system signals for graceful shutdown"""
    cleanup_on_shutdown()
    sys.exit(0)


if __name__ == "__main__":
    try:
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, handle_signal)
        signal.signal(signal.SIGTERM, handle_signal)
        
        # Initialize production infrastructure
        app_logger = initialize_production_infrastructure()
        
        # Verify system is ready
        verify_system_ready()
        
        # Log application configuration
        config = get_config()
        app_logger.info("Production constants loaded",
            audio_sample_rate=AUDIO_CONFIG["sample_rate"],
            vision_resolution=VISION_CONFIG["resolution"],
            compute_device=COMPUTE_CONFIG["whisper_device"],
            monitoring_enabled=bool(MONITORING_CONFIG),
        )
        
        # Start assistant with production configuration
        app_logger.info("Starting voice assistant")
        assistant = VoiceLoop()
        assistant.start_production()
        
    except KeyboardInterrupt:
        cleanup_on_shutdown()
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        if _logger:
            _logger.get_logger("main").log_error("Fatal application error", {
                "error": str(e),
                "error_type": type(e).__name__
            })
        import traceback
        traceback.print_exc()
        cleanup_on_shutdown()
        sys.exit(1)