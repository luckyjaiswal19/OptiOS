import pandas as pd
import matplotlib.pyplot as plt
from models.simulator import shared_simulator

# Load RL predictions log
df = pd.read_csv('rl_predictions.csv')

if df.empty:
    print("No RL predictions found.")
    exit()

accuracies = []
avg_waiting_times = []

# Mapping RL choices to simulator algorithm names
RL_TO_SIM = {
    'FCFS': 'FCFS',
    'SJF': 'SJF',
    'RR': 'Round Robin'
}

for idx, row in df.iterrows():
    # Randomize processes (or optionally recreate exact state if logged)
    shared_simulator.randomize_processes()
    
    # Simulate all algorithms
    fcfs = shared_simulator.fcfs()
    sjf = shared_simulator.sjf()
    rr = shared_simulator.round_robin()
    
    algos = [fcfs, sjf, rr]
    
    # Optimal algorithm for this state (lowest avg waiting time)
    best_algo = min(algos, key=lambda x: x['Average Waiting Time'])['Algorithm']
    
    # Map RL choice to simulator name
    rl_choice_sim = RL_TO_SIM.get(row['rl_choice'], row['rl_choice'])
    
    # Check if RL choice matches optimal
    is_correct = int(rl_choice_sim == best_algo)
    accuracies.append(is_correct)
    
    # Record waiting time for RL choice
    rl_wait_time = next(a['Average Waiting Time'] for a in algos if a['Algorithm'] == rl_choice_sim)
    avg_waiting_times.append(rl_wait_time)

# Overall accuracy
overall_accuracy = sum(accuracies) / len(accuracies) * 100
print(f"RL agent accuracy (choosing optimal algorithm): {overall_accuracy:.2f}%")

# Plot learning curve
plt.figure(figsize=(10,5))
plt.plot(avg_waiting_times, label='RL Chosen Algorithm Waiting Time', color='blue')
plt.xlabel('Logged Steps')
plt.ylabel('Average Waiting Time')
plt.title('RL Agent Learning Progress')
plt.legend()
plt.grid(True)
plt.show()
