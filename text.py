import pandas as pd
from models.simulator import OSSimulator, shared_simulator

# Load RL predictions log
df = pd.read_csv('rl_predictions.csv')

correct_count = 0
total = len(df)

for _, row in df.iterrows():
    # Recreate the system state
    shared_simulator.randomize_processes()
    # Here you could optionally fix ready_queue_size etc. if you logged more detailed process info

    # Simulate all algorithms
    fcfs = shared_simulator.fcfs()
    sjf = shared_simulator.sjf()
    rr = shared_simulator.round_robin()

    # Choose the algorithm with lowest average waiting time
    best_algo = min([fcfs, sjf, rr], key=lambda x: x['Average Waiting Time'])['Algorithm']

    if row['rl_choice'] == best_algo:
        correct_count += 1

accuracy = correct_count / total * 100
print(f"RL agent accuracy (choosing optimal algorithm): {accuracy:.2f}%")
