import csv
from datetime import datetime

def log_rl_prediction(state, rl_choice, log_file='rl_predictions.csv'):
    """
    Logs the current system state and RL agent's chosen action.
    """
    with open(log_file, 'a', newline='') as f:
        writer = csv.writer(f)
        # Write header if file is empty
        if f.tell() == 0:
            writer.writerow(['timestamp','ready_queue_size','avg_burst_time','avg_priority','memory_usage','rl_choice'])
        writer.writerow([
            datetime.utcnow().isoformat(),
            state[0],
            state[1],
            state[2],
            state[3],
            rl_choice
        ])
