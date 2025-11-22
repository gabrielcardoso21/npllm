"""
Monitoring and metrics for npllm
Resource usage tracking and health checks
"""

import psutil
import time
from typing import Dict, Any, Optional
from prometheus_client import Gauge, Counter, Histogram, start_http_server
from threading import Thread


class ResourceMonitor:
    """Monitor system resources (CPU, memory)"""
    
    def __init__(self, warning_threshold: float = 0.85):
        """
        Initialize resource monitor
        
        Args:
            warning_threshold: Memory warning threshold (0.0-1.0)
        """
        self.warning_threshold = warning_threshold
        self.process = psutil.Process()
        
        # Prometheus metrics
        self.memory_usage = Gauge('npllm_memory_usage_bytes', 'Memory usage in bytes')
        self.cpu_usage = Gauge('npllm_cpu_usage_percent', 'CPU usage percentage')
        self.request_count = Counter('npllm_requests_total', 'Total number of requests')
        self.request_latency = Histogram('npllm_request_latency_seconds', 'Request latency in seconds')
        self.error_count = Counter('npllm_errors_total', 'Total number of errors')
    
    def get_memory_usage(self) -> Dict[str, Any]:
        """Get current memory usage"""
        mem_info = self.process.memory_info()
        system_mem = psutil.virtual_memory()
        
        return {
            "process_memory_mb": mem_info.rss / 1024 / 1024,
            "system_memory_percent": system_mem.percent,
            "system_memory_available_mb": system_mem.available / 1024 / 1024,
            "system_memory_total_mb": system_mem.total / 1024 / 1024
        }
    
    def get_cpu_usage(self) -> Dict[str, Any]:
        """Get current CPU usage"""
        cpu_percent = self.process.cpu_percent(interval=1)
        system_cpu = psutil.cpu_percent(interval=1, percpu=True)
        
        return {
            "process_cpu_percent": cpu_percent,
            "system_cpu_percent": sum(system_cpu) / len(system_cpu),
            "system_cpu_per_core": system_cpu
        }
    
    def check_health(self) -> Dict[str, Any]:
        """Perform health check"""
        mem_usage = self.get_memory_usage()
        cpu_usage = self.get_cpu_usage()
        
        is_healthy = True
        warnings = []
        
        # Check memory
        if mem_usage["system_memory_percent"] > (self.warning_threshold * 100):
            is_healthy = False
            warnings.append(f"High memory usage: {mem_usage['system_memory_percent']:.1f}%")
        
        # Check CPU
        if cpu_usage["system_cpu_percent"] > 85:
            warnings.append(f"High CPU usage: {cpu_usage['system_cpu_percent']:.1f}%")
        
        return {
            "healthy": is_healthy,
            "memory": mem_usage,
            "cpu": cpu_usage,
            "warnings": warnings,
            "timestamp": time.time()
        }
    
    def update_metrics(self):
        """Update Prometheus metrics"""
        mem_usage = self.get_memory_usage()
        cpu_usage = self.get_cpu_usage()
        
        self.memory_usage.set(mem_usage["process_memory_mb"] * 1024 * 1024)
        self.cpu_usage.set(cpu_usage["process_cpu_percent"])
    
    def start_metrics_server(self, port: int = 9090):
        """Start Prometheus metrics server"""
        start_http_server(port)
        return f"Metrics server started on port {port}"


class HealthChecker:
    """Health check service"""
    
    def __init__(self, monitor: ResourceMonitor, check_interval: int = 60):
        """
        Initialize health checker
        
        Args:
            monitor: ResourceMonitor instance
            check_interval: Health check interval in seconds
        """
        self.monitor = monitor
        self.check_interval = check_interval
        self.running = False
        self.thread: Optional[Thread] = None
    
    def start(self):
        """Start health checking in background thread"""
        if self.running:
            return
        
        self.running = True
        self.thread = Thread(target=self._check_loop, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop health checking"""
        self.running = False
        if self.thread:
            self.thread.join()
    
    def _check_loop(self):
        """Health check loop"""
        while self.running:
            health = self.monitor.check_health()
            self.monitor.update_metrics()
            
            if not health["healthy"]:
                # Log warnings
                for warning in health["warnings"]:
                    print(f"WARNING: {warning}")
            
            time.sleep(self.check_interval)

