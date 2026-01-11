import threading
import collections
import sqlite3
import time
from datetime import datetime

class DataManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(DataManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, db_path='optios.db', history_len=200):
        # Prevent re-initialization
        if hasattr(self, 'initialized') and self.initialized:
            return
        
        self.db_path = db_path
        self.history_len = history_len
        # In-memory storage for fast access by RL agent
        self.live_data = collections.deque(maxlen=history_len)
        self.data_lock = threading.Lock()
        
        # Initialize DB
        self._init_db()
        self.initialized = True
        print("🟢 DataManager initialized")

    def _init_db(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    cpu_percent REAL,
                    memory_usage REAL,
                    ready_queue_size INTEGER,
                    avg_burst_time REAL,
                    avg_priority REAL
                )
            ''')
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"🔴 DataManager DB Init Error: {e}")

    def add_record(self, record):
        """
        record: dict containing keys matching the schema
        """
        with self.data_lock:
            self.live_data.append(record)
        
        # Persist to DB asynchronously or synchronously? 
        # For simplicity and safety in this scale, synchronous is fine for SQLite (WAL mode is better but keep it simple)
        if record:
             self._persist_record(record)

    def _persist_record(self, record):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO system_stats (timestamp, cpu_percent, memory_usage, ready_queue_size, avg_burst_time, avg_priority)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                record.get('timestamp', datetime.utcnow().isoformat()),
                record.get('cpu_percent', 0.0),
                record.get('memory_usage', 0.0),
                record.get('ready_queue_size', 0),
                record.get('avg_burst_time', 0.0),
                record.get('avg_priority', 0.0)
            ))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"🔴 DB Write Error: {e}")

    def get_latest(self):
        with self.data_lock:
            if self.live_data:
                return self.live_data[-1]
            return None

    def get_history(self):
        with self.data_lock:
            return list(self.live_data)

# Shared instance
shared_data_manager = DataManager()
