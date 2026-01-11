import threading
import psutil
import random
import time
from datetime import datetime
from utils.data_manager import shared_data_manager

class LiveMonitor:
    def __init__(self, interval=5):
        self.interval = interval
        self.running = False
        self.thread = None

    def _collect_data(self):
        while self.running:
            try:
                cpu_percent = psutil.cpu_percent(interval=1) # This blocks for 1s
                num_procs = len(psutil.pids())
                memory = psutil.virtual_memory().percent

                record = {
                    'timestamp': datetime.utcnow().isoformat(),
                    'ready_queue_size': int(num_procs),
                    'avg_burst_time': float(random.uniform(5, 50) * (cpu_percent / 100)),
                    'avg_priority': float(random.uniform(1, 10)),
                    'memory_usage': float(memory),
                    'cpu_percent': float(cpu_percent)
                }

                # Push to DataManager
                shared_data_manager.add_record(record)
                
                print(f"[LiveMonitor] Data collected: CPU={cpu_percent}% Mem={memory}%")

            except Exception as e:
                print("[LiveMonitor] error:", e)
            
            # Since cpu_percent(interval=1) already waits 1s, we adjust sleep
            sleep_time = max(0, self.interval - 1)
            time.sleep(sleep_time)

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._collect_data, daemon=True)
            self.thread.start()
            print("🟢 LiveMonitor started")

    def stop(self):
        self.running = False
        print("🔴 LiveMonitor stopped")
