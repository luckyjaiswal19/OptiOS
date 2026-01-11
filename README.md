# OptiOS: Intelligent OS Simulation & Monitoring

OptiOS is a sophisticated Operative System simulator and real-time monitoring tool powered by Reinforcement Learning. It visualizes CPU scheduling algorithms and demonstrates how an AI agent can optimize system performance dynamically.

![OptiOS Dashboard](static/img/dashboard_preview.png)
*(Note: Add a screenshot of the dashboard here if available, or remove this line)*

## 🚀 Features

- **Real-time System Monitoring**: Live tracking of CPU usage, Memory consumption, and active processes.
- **AI-Powered Scheduling**: A Deep Q-Network (Reinforcement Learning) agent that dynamically selects the best scheduling algorithm (FCFS, SJF, Round Robin) based on current system state.
- **Interactive Dashboard**: Premium UI with glassmorphism design, real-time charts (Chart.js), and dynamic comparisons.
- **Thread-Safe Architecture**: Built with a robust `DataManager` using in-memory deques and SQLite for persistence, ensuring zero race conditions.

## 🛠️ Tech Stack

- **Backend**: Python, Flask, Pandas, SQLite
- **Frontend**: HTML5, Vanilla CSS (Glassmorphism), JavaScript, Chart.js
- **AI/ML**: Reinforcement Learning (Q-Learning), NumPy
- **System**: psutil for hardware metrics

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/luckyjaiswal19/OptiOS.git
   cd OptiOS
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the Dashboard**:
   Open your browser and navigate to `http://localhost:5000`.

## 🧠 How It Works

1. **Monitor**: The `LiveMonitor` captures real-time system metrics (CPU, Memory, Process count).
2. **Simulate**: The `RLSchedulerAgent` analyzes the state and predicts the optimal scheduling algorithm to minimize waiting time and turnaround time.
3. **Learn**: The agent continuously trains in the background, improving its decision-making over time based on simulated rewards.

## 📂 Project Structure

```
OptiOS/
├── app.py                 # Main Flask Application
├── optios.db              # SQLite Database (History)
├── requirements.txt       # Python Dependencies
├── static/                # CSS, Images, JS
├── templates/             # HTML Templates
├── routes/                # Blueprint Routes
├── models/                # Simulation Models
└── utils/                 # Helpers (RL Agent, Monitor, DataManager)
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open-source and available under the MIT License.
