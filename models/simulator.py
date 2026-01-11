import pandas as pd
import random

class Process:
    def __init__(self, pid, burst_time, priority, memory, arrival_time):
        self.pid = pid
        self.burst_time = burst_time
        self.priority = priority
        self.memory = memory
        self.arrival_time = arrival_time
        self.waiting_time = 0
        self.turnaround_time = 0

class OSSimulator:
    def __init__(self):
        self.randomize_processes()

    def randomize_processes(self, num_processes=10):
        self.processes = []
        for i in range(1, num_processes+1):
            burst = random.randint(2, 10)
            priority = random.randint(1, 5)
            memory = random.randint(50, 300)
            arrival = random.randint(0, 9)
            self.processes.append(Process(i, burst, priority, memory, arrival))

    def fcfs(self):
        time = 0
        for p in self.processes:
            if time < p.arrival_time:
                time = p.arrival_time
            p.waiting_time = time - p.arrival_time
            time += p.burst_time
            p.turnaround_time = p.waiting_time + p.burst_time
        return self._metrics("FCFS")

    def sjf(self):
        time = 0
        completed = []
        processes = sorted(self.processes, key=lambda x: x.arrival_time)
        ready = []
        while len(completed) < len(processes):
            for p in processes:
                if p.arrival_time <= time and p not in ready and p not in completed:
                    ready.append(p)
            if ready:
                ready.sort(key=lambda x: x.burst_time)
                current = ready.pop(0)
                current.waiting_time = time - current.arrival_time
                time += current.burst_time
                current.turnaround_time = current.waiting_time + current.burst_time
                completed.append(current)
            else:
                time += 1
        return self._metrics("SJF")

    def round_robin(self, quantum=3):
        queue = []
        time = 0
        remaining = {p.pid: p.burst_time for p in self.processes}
        while True:
            for p in self.processes:
                if p.arrival_time <= time and p not in queue and remaining[p.pid] > 0:
                    queue.append(p)
            if not queue:
                if all(v == 0 for v in remaining.values()):
                    break
                time += 1
                continue
            current = queue.pop(0)
            exec_time = min(quantum, remaining[current.pid])
            remaining[current.pid] -= exec_time
            time += exec_time
            for p in self.processes:
                if p != current and p.arrival_time <= time and remaining[p.pid] > 0:
                    if p not in queue:
                        queue.append(p)
            if remaining[current.pid] == 0:
                current.turnaround_time = time - current.arrival_time
                current.waiting_time = current.turnaround_time - current.burst_time
        return self._metrics("Round Robin")

    def _metrics(self, name):
        df = pd.DataFrame([{
            'PID': p.pid,
            'Burst': p.burst_time,
            'Waiting': p.waiting_time,
            'Turnaround': p.turnaround_time,
            'Priority': p.priority,
            'Memory': p.memory
        } for p in self.processes])
        return {
            'Algorithm': name,
            'Average Waiting Time': round(df['Waiting'].mean(), 2),
            'Average Turnaround Time': round(df['Turnaround'].mean(), 2)
        }

# shared simulator instance
shared_simulator = OSSimulator()
