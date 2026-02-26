#!/usr/bin/env python3
"""
GPU-Optimized Multimodal Voice Assistant
Production entry point with CUDA support, logging, monitoring, and error handling
"""

# ============================================================
# CRITICAL: OPENMP + CUDA FIX (MUST BE FIRST)
# ============================================================

import os

# Fix Intel OpenMP duplicate runtime crash
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Restrict to GPU 0
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# Optional: reduce OpenMP thread conflicts
os.environ["OMP_NUM_THREADS"] = "1"

# ============================================================
# STANDARD IMPORTS
# ============================================================

import sys
import signal

# ============================================================
# PRODUCTION INFRASTRUCTURE
# ============================================================

from config_production import (
    get_config,
    create_directories,
    AUDIO_CONFIG,
    VISION_CONFIG,
    COMPUTE_CONFIG,
    MONITORING_CONFIG,
)

from infrastructure.production_logger import get_production_logger
from infrastructure.system_monitor import (
    get_health_monitor,
    get_performance_tracker,
    get_resource_cleaner,
)
from infrastructure.error_handling import retry_with_backoff, RetryConfig

# ============================================================
# APPLICATION IMPORT
# ============================================================

from voice.voice_loop import VoiceLoop

# ============================================================
# GLOBAL INFRASTRUCTURE OBJECTS
# ============================================================

_logger = None
_health_monitor = None
_performance_tracker = None
_resource_cleaner = None


# ============================================================
# INITIALIZATION
# ============================================================

def initialize_production_infrastructure():
    global _logger, _health_monitor, _performance_tracker, _resource_cleaner

    print("\n" + "=" * 70)
    print("🚀 GPU-OPTIMIZED MULTIMODAL VOICE ASSISTANT (PRODUCTION)")
    print("=" * 70 + "\n")

    # 1️⃣ Create directories
    print("📁 Creating directory structure...")
    create_directories()

    # 2️⃣ Initialize logger
    print("📝 Initializing production logging...")
    _logger = get_production_logger()
    app_logger = _logger.get_logger("main")

    app_logger.info("Application startup initiated")

    # 3️⃣ Health monitor
    print("💚 Initializing system health monitoring...")
    _health_monitor = get_health_monitor()
    _health_monitor.start()

    # 4️⃣ Performance tracker
    print("⚡ Initializing performance tracking...")
    _performance_tracker = get_performance_tracker()

    # 5️⃣ Resource cleaner
    print("🧹 Initializing resource management...")
    _resource_cleaner = get_resource_cleaner()

    print()
    return app_logger


# ============================================================
# SYSTEM VERIFICATION
# ============================================================

@retry_with_backoff(RetryConfig(max_attempts=3, initial_delay=1.0))
def verify_system_ready():
    import torch

    cuda_available = torch.cuda.is_available()

    print("📊 System Configuration:")
    print(f"   GPU Available: {'✅ Yes' if cuda_available else '❌ No'}")

    app_logger = _logger.get_logger("main")

    if cuda_available:
        device_name = torch.cuda.get_device_name(0)
        cuda_version = torch.version.cuda
        pytorch_version = torch.__version__

        print(f"   GPU Device: {device_name}")
        print(f"   CUDA Version: {cuda_version}")
        print(f"   PyTorch Version: {pytorch_version}")

        app_logger.info(
            "GPU configuration verified",
            extra={
                "gpu_device": device_name,
                "cuda_version": cuda_version,
                "pytorch_version": pytorch_version,
            },
        )
    else:
        app_logger.warning(
            "CUDA not available, falling back to CPU"
        )

    print()
    return cuda_available


# ============================================================
# CLEAN SHUTDOWN
# ============================================================

def cleanup_on_shutdown():
    print("\n🛑 Shutting down application...\n")

    try:
        app_logger = _logger.get_logger("main") if _logger else None

        if _resource_cleaner:
            print("🧹 Cleaning up resources...")
            _resource_cleaner.cleanup_all()

        if _health_monitor:
            print("💚 Stopping health monitor...")
            _health_monitor.stop()

        if app_logger:
            app_logger.info("Application shutdown complete")

        print("\n✅ All systems shut down gracefully")

    except Exception as e:
        print(f"\n⚠️  Error during shutdown: {e}")


def handle_signal(signum, frame):
    cleanup_on_shutdown()
    sys.exit(0)


# ============================================================
# MAIN ENTRY POINT
# ============================================================

if __name__ == "__main__":
    try:
        # Graceful shutdown signals
        signal.signal(signal.SIGINT, handle_signal)
        signal.signal(signal.SIGTERM, handle_signal)

        # Initialize infrastructure
        app_logger = initialize_production_infrastructure()

        # Verify GPU / system
        verify_system_ready()

        # Log configuration
        config = get_config()

        app_logger.info(
            "Production constants loaded",
            extra={
                "audio_sample_rate": AUDIO_CONFIG["sample_rate"],
                "vision_resolution": VISION_CONFIG["resolution"],
                "compute_device": COMPUTE_CONFIG["whisper_device"],
                "monitoring_enabled": bool(MONITORING_CONFIG),
            },
        )

        app_logger.info("Starting voice assistant")

        # Start assistant
        assistant = VoiceLoop()
        assistant.start_production()

    except KeyboardInterrupt:
        cleanup_on_shutdown()

    except Exception as e:
        print(f"\n❌ Fatal error: {e}")

        if _logger:
            _logger.get_logger("main").error(
                "Fatal application error",
                exc_info=True
            )

        cleanup_on_shutdown()
        sys.exit(1)