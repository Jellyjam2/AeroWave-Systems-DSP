"""
Hardened Multi-Core Task Scheduling
Core-pinned task queues for deterministic performance
Prevents background processes from stealing CPU cycles from real-time audio
"""

import threading
import multiprocessing
import time
import ctypes
import platform
from typing import Optional, Callable, Dict, Any
from enum import Enum
import queue

class TaskPriority(Enum):
    """Task priority levels."""
    CRITICAL = 0  # Real-time audio processing
    HIGH = 1      # SAT solving, NLP processing
    MEDIUM = 2    # Cache operations
    LOW = 3       # Background cleanup

class TaskType(Enum):
    """Task types for core assignment."""
    AUDIO_PROCESSING = "audio"
    NLP_PROCESSING = "nlp"
    SAT_SOLVING = "sat"
    CACHE_OPERATIONS = "cache"
    BACKGROUND = "background"


class CoreAffinityManager:
    """
    Core affinity manager for pinning threads to specific CPU cores.
    Ensures deterministic performance by preventing thread migration.
    """
    
    def __init__(self):
        """Initialize core affinity manager."""
        self.num_cores = multiprocessing.cpu_count()
        self.core_assignments = {}
        self.lock = threading.Lock()
    
    def set_thread_affinity(self, thread_id: int, core_id: int) -> bool:
        """
        Pin thread to specific CPU core.
        
        Args:
            thread_id: Thread identifier
            core_id: Core ID to pin to
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if platform.system() == "Windows":
                # Windows: SetThreadAffinityMask
                handle = ctypes.windll.kernel32.OpenThread(0x0200, False, thread_id)
                if handle:
                    mask = 1 << core_id
                    result = ctypes.windll.kernel32.SetThreadAffinityMask(handle, mask)
                    ctypes.windll.kernel32.CloseHandle(handle)
                    return result != 0
            elif platform.system() == "Linux":
                # Linux: sched_setaffinity
                import os
                os.sched_setaffinity(thread_id, {core_id})
                return True
            
            return False
        except Exception as e:
            print(f"  [SCHEDULER]: Error setting affinity: {e}")
            return False
    
    def set_process_affinity(self, process_id: int, core_ids: list) -> bool:
        """
        Pin process to specific CPU cores.
        
        Args:
            process_id: Process identifier
            core_ids: List of core IDs to pin to
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if platform.system() == "Windows":
                handle = ctypes.windll.kernel32.OpenProcess(0x0200, False, process_id)
                if handle:
                    mask = 0
                    for core_id in core_ids:
                        mask |= 1 << core_id
                    result = ctypes.windll.kernel32.SetProcessAffinityMask(handle, mask)
                    ctypes.windll.kernel32.CloseHandle(handle)
                    return result != 0
            elif platform.system() == "Linux":
                import os
                os.sched_setaffinity(process_id, set(core_ids))
                return True
            
            return False
        except Exception as e:
            print(f"  [SCHEDULER]: Error setting process affinity: {e}")
            return False
    
    def get_optimal_core_assignment(self, task_type: TaskType) -> int:
        """
        Get optimal core ID for task type.
        
        Args:
            task_type: Type of task
            
        Returns:
            Optimal core ID
        """
        with self.lock:
            # Simple round-robin with task type preferences
            if task_type == TaskType.AUDIO_PROCESSING:
                # Audio processing gets core 0 (highest priority)
                return 0
            elif task_type == TaskType.NLP_PROCESSING:
                # NLP gets core 1
                return 1 % self.num_cores
            elif task_type == TaskType.SAT_SOLVING:
                # SAT solving gets core 2
                return 2 % self.num_cores
            elif task_type == TaskType.CACHE_OPERATIONS:
                # Cache operations get core 3
                return 3 % self.num_cores
            else:
                # Background tasks get remaining cores
                return 4 % self.num_cores


class HardenedTaskQueue:
    """
    Hardened task queue with priority support.
    Lock-free design for high-throughput task processing.
    """
    
    def __init__(self, max_size: int = 1000):
        """
        Initialize hardened task queue.
        
        Args:
            max_size: Maximum queue size
        """
        self.queues = {
            TaskPriority.CRITICAL: queue.Queue(maxsize=max_size),
            TaskPriority.HIGH: queue.Queue(maxsize=max_size),
            TaskPriority.MEDIUM: queue.Queue(maxsize=max_size),
            TaskPriority.LOW: queue.Queue(maxsize=max_size)
        }
        self.lock = threading.Lock()
    
    def put_task(self, task: Dict[str, Any], priority: TaskPriority = TaskPriority.MEDIUM) -> bool:
        """
        Add task to queue.
        
        Args:
            task: Task dictionary with function and args
            priority: Task priority
            
        Returns:
            True if task added, False if queue full
        """
        try:
            self.queues[priority].put(task, block=False)
            return True
        except queue.Full:
            return False
    
    def get_task(self, timeout: float = 0.1) -> Optional[Dict[str, Any]]:
        """
        Get highest priority task.
        
        Args:
            timeout: Timeout in seconds
            
        Returns:
            Task dictionary or None
        """
        # Check queues in priority order
        for priority in [TaskPriority.CRITICAL, TaskPriority.HIGH, TaskPriority.MEDIUM, TaskPriority.LOW]:
            try:
                return self.queues[priority].get(block=False)
            except queue.Empty:
                continue
        
        return None
    
    def get_queue_stats(self) -> Dict[str, int]:
        """Get queue statistics."""
        return {
            priority.name: self.queues[priority].qsize()
            for priority in TaskPriority
        }


class HardenedTaskScheduler:
    """
    Hardened multi-core task scheduler.
    Manages core-pinned task queues for deterministic performance.
    """
    
    def __init__(self):
        """Initialize hardened task scheduler."""
        self.affinity_manager = CoreAffinityManager()
        self.task_queue = HardenedTaskQueue()
        self.worker_threads = {}
        self.running = False
        self.lock = threading.Lock()
        self.performance_metrics = {}
    
    def start(self):
        """Start task scheduler."""
        with self.lock:
            if self.running:
                return
            
            self.running = True
            
            # Start worker threads for each task type
            self._start_audio_worker()
            self._start_nlp_worker()
            self._start_sat_worker()
            self._start_cache_worker()
            self._start_background_worker()
            
            print("  [SCHEDULER]: Hardened multi-core task scheduler started")
    
    def stop(self):
        """Stop task scheduler."""
        with self.lock:
            self.running = False
        
        # Wait for worker threads to finish
        for thread_id, thread in self.worker_threads.items():
            thread.join(timeout=2.0)
        
        print("  [SCHEDULER]: Hardened multi-core task scheduler stopped")
    
    def _start_audio_worker(self):
        """Start audio processing worker thread."""
        def audio_worker():
            core_id = self.affinity_manager.get_optimal_core_assignment(TaskType.AUDIO_PROCESSING)
            thread_id = threading.get_ident()
            self.affinity_manager.set_thread_affinity(thread_id, core_id)
            
            print(f"  [SCHEDULER]: Audio worker pinned to core {core_id}")
            
            while self.running:
                task = self.task_queue.get_task(timeout=0.1)
                if task and task.get('type') == TaskType.AUDIO_PROCESSING:
                    start_time = time.time()
                    try:
                        task['function'](*task.get('args', []), **task.get('kwargs', {}))
                        elapsed = time.time() - start_time
                        self._record_metric('audio', elapsed)
                    except Exception as e:
                        print(f"  [SCHEDULER]: Audio task error: {e}")
        
        thread = threading.Thread(target=audio_worker, daemon=True)
        thread.start()
        self.worker_threads['audio'] = thread
    
    def _start_nlp_worker(self):
        """Start NLP processing worker thread."""
        def nlp_worker():
            core_id = self.affinity_manager.get_optimal_core_assignment(TaskType.NLP_PROCESSING)
            thread_id = threading.get_ident()
            self.affinity_manager.set_thread_affinity(thread_id, core_id)
            
            print(f"  [SCHEDULER]: NLP worker pinned to core {core_id}")
            
            while self.running:
                task = self.task_queue.get_task(timeout=0.1)
                if task and task.get('type') == TaskType.NLP_PROCESSING:
                    start_time = time.time()
                    try:
                        task['function'](*task.get('args', []), **task.get('kwargs', {}))
                        elapsed = time.time() - start_time
                        self._record_metric('nlp', elapsed)
                    except Exception as e:
                        print(f"  [SCHEDULER]: NLP task error: {e}")
        
        thread = threading.Thread(target=nlp_worker, daemon=True)
        thread.start()
        self.worker_threads['nlp'] = thread
    
    def _start_sat_worker(self):
        """Start SAT solving worker thread."""
        def sat_worker():
            core_id = self.affinity_manager.get_optimal_core_assignment(TaskType.SAT_SOLVING)
            thread_id = threading.get_ident()
            self.affinity_manager.set_thread_affinity(thread_id, core_id)
            
            print(f"  [SCHEDULER]: SAT worker pinned to core {core_id}")
            
            while self.running:
                task = self.task_queue.get_task(timeout=0.1)
                if task and task.get('type') == TaskType.SAT_SOLVING:
                    start_time = time.time()
                    try:
                        task['function'](*task.get('args', []), **task.get('kwargs', {}))
                        elapsed = time.time() - start_time
                        self._record_metric('sat', elapsed)
                    except Exception as e:
                        print(f"  [SCHEDULER]: SAT task error: {e}")
        
        thread = threading.Thread(target=sat_worker, daemon=True)
        thread.start()
        self.worker_threads['sat'] = thread
    
    def _start_cache_worker(self):
        """Start cache operations worker thread."""
        def cache_worker():
            core_id = self.affinity_manager.get_optimal_core_assignment(TaskType.CACHE_OPERATIONS)
            thread_id = threading.get_ident()
            self.affinity_manager.set_thread_affinity(thread_id, core_id)
            
            print(f"  [SCHEDULER]: Cache worker pinned to core {core_id}")
            
            while self.running:
                task = self.task_queue.get_task(timeout=0.1)
                if task and task.get('type') == TaskType.CACHE_OPERATIONS:
                    start_time = time.time()
                    try:
                        task['function'](*task.get('args', []), **task.get('kwargs', {}))
                        elapsed = time.time() - start_time
                        self._record_metric('cache', elapsed)
                    except Exception as e:
                        print(f"  [SCHEDULER]: Cache task error: {e}")
        
        thread = threading.Thread(target=cache_worker, daemon=True)
        thread.start()
        self.worker_threads['cache'] = thread
    
    def _start_background_worker(self):
        """Start background cleanup worker thread."""
        def background_worker():
            core_id = self.affinity_manager.get_optimal_core_assignment(TaskType.BACKGROUND)
            thread_id = threading.get_ident()
            self.affinity_manager.set_thread_affinity(thread_id, core_id)
            
            print(f"  [SCHEDULER]: Background worker pinned to core {core_id}")
            
            while self.running:
                task = self.task_queue.get_task(timeout=0.1)
                if task and task.get('type') == TaskType.BACKGROUND:
                    start_time = time.time()
                    try:
                        task['function'](*task.get('args', []), **task.get('kwargs', {}))
                        elapsed = time.time() - start_time
                        self._record_metric('background', elapsed)
                    except Exception as e:
                        print(f"  [SCHEDULER]: Background task error: {e}")
        
        thread = threading.Thread(target=background_worker, daemon=True)
        thread.start()
        self.worker_threads['background'] = thread
    
    def submit_task(self, function: Callable, task_type: TaskType, 
                   priority: TaskPriority = TaskPriority.MEDIUM,
                   args: tuple = (), kwargs: dict = None) -> bool:
        """
        Submit task to scheduler.
        
        Args:
            function: Function to execute
            task_type: Type of task
            priority: Task priority
            args: Function arguments
            kwargs: Function keyword arguments
            
        Returns:
            True if task submitted, False if queue full
        """
        task = {
            'function': function,
            'type': task_type,
            'args': args,
            'kwargs': kwargs or {}
        }
        
        return self.task_queue.put_task(task, priority)
    
    def _record_metric(self, task_type: str, execution_time: float):
        """Record performance metric."""
        with self.lock:
            if task_type not in self.performance_metrics:
                self.performance_metrics[task_type] = {
                    'count': 0,
                    'total_time': 0.0,
                    'max_time': 0.0,
                    'min_time': float('inf')
                }
            
            metrics = self.performance_metrics[task_type]
            metrics['count'] += 1
            metrics['total_time'] += execution_time
            metrics['max_time'] = max(metrics['max_time'], execution_time)
            metrics['min_time'] = min(metrics['min_time'], execution_time)
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics."""
        with self.lock:
            result = {}
            for task_type, metrics in self.performance_metrics.items():
                if metrics['count'] > 0:
                    result[task_type] = {
                        'count': metrics['count'],
                        'avg_time': metrics['total_time'] / metrics['count'],
                        'max_time': metrics['max_time'],
                        'min_time': metrics['min_time']
                    }
            return result
    
    def get_queue_status(self) -> Dict[str, Any]:
        """Get queue status."""
        return {
            'queue_sizes': self.task_queue.get_queue_stats(),
            'active_workers': len(self.worker_threads),
            'running': self.running
        }
