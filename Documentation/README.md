**# Brute Force Simulator (Dictionary Attack Engine)**



An offensive security testing utility designed to demonstrate the mechanics of credential-stuffing and dictionary-based brute-force attacks. This tool is intended for auditoring the rate-limiting and account-lockout policies of authentication endpoints.



**## Project Structure**

```text

brute-force-sim/

├── app.py                # Attack Engine \\\& Session Logger

├── logs/                 # Directory for Audit Trails (.txt)

├── requirements.txt      # Dependencies

├── static/

│   ├── css/style.css     # Red-Team Operational UI

│   └── js/main.js        # Attack Sequence \\\& UI Handlers

└── templates/

\&nbsp;   └── index.html        # Attack Dashboard



\*\*Operational Methodology\*\*

\* \*\*Dictionary Attack\*\*: Ingests user-provided wordlists to systematically guess credentials against a target REST API.
\* \*\*REST Analysis\*\*: Evaluates HTTP response codes (e.g., 200 vs 401) to identify successful authentication bypasses.
\* \*\*Session Logging\*\*: Methodically records every attempt, timestamp, and result into the logs/ directory for post-attack analysis and reporting.
\* \*\*Speed Control\*\*: Implements a controlled delay between attempts to simulate real-world request pading and avoid crashing local target servers.



\*\*Setup \\\& Execution\*\*



Initialize Engine:

├── python app.py

\&nbsp;	├── \*The system operates on Port 5007.\*



Conduct Audit:

\* Ensure the target system (e.g., Project #4 Login System) is running.
\* Enter the target URL, target username, and a wordlist of potential passwords.
\* Click "EXECUTE" to begin the sequence.





\*\*Building the Portable Attack Tool\*\*



Windows Command: pyinstaller --onefile --noconsole --add-data "templates;templates" --add-data "static;static" app.py



\*\*Defensive Insight\*\*

Running this tool against your own projects illustrates exactly why complex passwords and exponential back-off (lockout) policies are critical. A short password can be identified in milliseconds, while a properly secured endpoint will resist such automated attempts.


