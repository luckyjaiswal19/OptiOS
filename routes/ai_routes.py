from flask import Blueprint, render_template, jsonify
from models.simulator import shared_simulator
from utils.rl_agent import shared_rl_agent
from utils.logger import log_rl_prediction
import pandas as pd

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/ai_dashboard')
def ai_dashboard():
    return render_template('ai_dashboard.html')

@ai_bp.route('/predict_live')
def predict_live():
    from utils.data_manager import shared_data_manager
    
    # Get latest from DataManager
    last = shared_data_manager.get_latest()
    
    if last:
        state = [
            int(last.get('ready_queue_size',0)),
            float(last.get('avg_burst_time',0)),
            float(last.get('avg_priority',0)),
            float(last.get('memory_usage',0))
        ]
    else:
        state = [0,0,0,0]

    rl_choice = shared_rl_agent.best_algorithm_for_state(state)

    # Log RL prediction
    log_rl_prediction(state, rl_choice)

    # Simulate algorithms for comparison
    shared_simulator.randomize_processes()
    fcfs = shared_simulator.fcfs()
    shared_simulator.randomize_processes()
    sjf = shared_simulator.sjf()
    shared_simulator.randomize_processes()
    rr = shared_simulator.round_robin()

    return jsonify({
        "rl_choice": rl_choice,
        "state": {
            "ready_queue_size": int(state[0]),
            "avg_burst_time": float(state[1]),
            "avg_priority": float(state[2]),
            "memory_usage": float(state[3])
        },
        "comparisons": [
            {"Algorithm": fcfs['Algorithm'], "Average Waiting Time": fcfs['Average Waiting Time'], "Average Turnaround Time": fcfs['Average Turnaround Time']},
            {"Algorithm": sjf['Algorithm'], "Average Waiting Time": sjf['Average Waiting Time'], "Average Turnaround Time": sjf['Average Turnaround Time']},
            {"Algorithm": rr['Algorithm'], "Average Waiting Time": rr['Average Waiting Time'], "Average Turnaround Time": rr['Average Turnaround Time']}
        ]
    })
