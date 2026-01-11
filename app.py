from flask import Flask
import psutil
import os
from routes.home_routes import home_bp
from routes.ai_routes import ai_bp
from utils.rl_agent import start_continuous_rl_training
from utils.live_monitor import LiveMonitor
from utils.data_manager import shared_data_manager

app = Flask(__name__)

# Register blueprints
app.register_blueprint(home_bp)
app.register_blueprint(ai_bp)

# Start background processes ONLY if we are in the main process (reloader safety)
# The reloader spawns a child process. We want threads only in that child process or the main one if reloader is off.
# WERKZEUG_RUN_MAIN is set by Flask when it spawns the child 'reloader' process.
monitor = LiveMonitor(interval=5)
rl_stop_event = None

if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    monitor.start()
    rl_stop_event = start_continuous_rl_training(interval=5)

# Inject context variables globally for templates
@app.context_processor
def inject_status():
    return {
        'cpu_count': psutil.cpu_count(logical=True),
        'monitor_running': 'Yes' if monitor.running else 'No',
        'rl_running': 'Yes' if rl_stop_event and not rl_stop_event.is_set() else 'No'
    }

if __name__ == '__main__':
    print("🟢 Flask app starting...")
    app.run(debug=True, port=5001)
