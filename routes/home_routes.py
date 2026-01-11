from flask import Blueprint, render_template, jsonify
import psutil
import random

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    return render_template('home.html')

@home_bp.route('/live')
def live():
    cpu = psutil.cpu_percent(interval=0.2)
    memory = psutil.virtual_memory().percent
    procs = len(psutil.pids())
    avg_burst = random.uniform(5,50) * (cpu / 100)
    avg_priority = random.uniform(1,10)
    return jsonify({
        'cpu': round(cpu,2),
        'memory': round(memory,2),
        'processes': int(procs),
        'avg_burst_time': round(avg_burst,2),
        'avg_priority': round(avg_priority,2)
    })
