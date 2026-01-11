import numpy as np
import random
import threading
import time
import pandas as pd

# Actions -> scheduling algorithms
ACTION_MAP = {0: 'FCFS', 1: 'SJF', 2: 'RR'}

class RLSchedulerAgent:
    def __init__(self, n_states=200, alpha=0.2, gamma=0.9, epsilon=0.25):
        self.n_states = n_states
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        # Q-table: n_states x n_actions
        self.q_table = np.zeros((n_states, len(ACTION_MAP)))
        self.lock = threading.Lock()

    def _state_index(self, state):
        # state: [ready_queue_size, avg_burst_time, avg_priority, memory_usage]
        # Normalize components and combine to single index.
        rq = min(int(state[0]), 100)   # clamp
        burst = min(int(state[1]), 100)
        mem = min(int(state[3]), 100)
        # simple hashing into range
        idx = (rq * 3 + burst * 5 + mem * 7) % self.n_states
        return idx

    def choose_action(self, state):
        idx = self._state_index(state)
        with self.lock:
            if random.random() < self.epsilon:
                return random.randint(0, len(ACTION_MAP)-1)
            return int(np.argmax(self.q_table[idx]))

    def action_name(self, action_idx):
        return ACTION_MAP.get(action_idx, 'SJF')

    def update(self, state, action, reward, next_state):
        s = self._state_index(state)
        ns = self._state_index(next_state)
        with self.lock:
            old = self.q_table[s, action]
            best_next = np.max(self.q_table[ns])
            new = old + self.alpha * (reward + self.gamma * best_next - old)
            self.q_table[s, action] = new

    def best_algorithm_for_state(self, state):
        idx = self._state_index(state)
        with self.lock:
            action_idx = int(np.argmax(self.q_table[idx]))
        return self.action_name(action_idx)

# single shared agent used by routes and trainer
shared_rl_agent = RLSchedulerAgent()

# Continuous trainer: runs in background, reads csv and updates Q-table incrementally
# Continuous trainer: runs in background, reads data from DataManager and updates Q-table incrementally
def _continuous_rl_loop(agent, interval, stop_event):
    from utils.data_manager import shared_data_manager
    
    last_processed_count = 0
    
    while not stop_event.is_set():
        try:
            history = shared_data_manager.get_history()
            current_count = len(history)
            
            if current_count < 2 or current_count <= last_processed_count:
                time.sleep(interval)
                continue

            # Process new records
            # ideally we process from last_processed_count to current_count
            # For simplicity, we just iterate through the newly added slice
            # But since deque might drop old ones, simple indexing is tricky. 
            # We can just iterate the whole small history (200 items) and update. 
            # But updating Q-table multiple times on same data is bad if not careful with alpha.
            # Rationale for this assignment: just pick the last few items to train on to simulate online learning.
            
            # Use the last 10 records for training step to keep it fresh
            training_batch = history[-10:] if len(history) > 10 else history
            
            for i in range(len(training_batch)-1):
                s = training_batch[i]
                n = training_batch[i+1]
                
                state = [s.get('ready_queue_size',0), s.get('avg_burst_time',0), s.get('avg_priority',0), s.get('memory_usage',0)]
                next_state = [n.get('ready_queue_size',0), n.get('avg_burst_time',0), n.get('avg_priority',0), n.get('memory_usage',0)]
                
                action = agent.choose_action(state) # Off-policy or On-policy? Q-learning is off-policy.
                
                # Reward design
                reward = 0.0
                reward += (state[0] - next_state[0]) * 0.5
                reward += (state[1] - next_state[1]) * 0.2
                reward += (state[3] - next_state[3]) * 0.1
                reward -= (next_state[0] * 0.01)
                
                agent.update(state, action, reward, next_state)
            
            last_processed_count = current_count
            
            # decay epsilon slowly
            with agent.lock:
                agent.epsilon = max(0.02, agent.epsilon * 0.999)
                
        except Exception as e:
            print("[RL Trainer] error:", e)
        time.sleep(interval)

def start_continuous_rl_training(interval=5):
    stop_event = threading.Event()
    thread = threading.Thread(target=_continuous_rl_loop, args=(shared_rl_agent, interval, stop_event), daemon=True)
    thread.start()
    print("🧠 Continuous RL training started (background thread)")
    return stop_event
