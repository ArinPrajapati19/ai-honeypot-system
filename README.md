# AI-Powered Honeypot System for Threat Detection

## Overview
This project is an AI-assisted honeypot system designed to capture attacker activity and analyze malicious behavior using machine learning techniques.

It uses a simulated SSH/Telnet environment to collect real attack data and processes it through a custom-built pipeline for anomaly detection.

---

## Architecture

### 🛡️ Honeypot Layer (Data Source)
- Uses Cowrie honeypot to simulate SSH/Telnet services
- Captures attacker interactions and generates logs (`cowrie.json`)

---

### 📊 Data Processing Layer
- Implemented using Python
- Parses raw logs and extracts meaningful features
- Key file:
  - `log_reader.py` → processes and structures log data

---

### 🤖 Machine Learning Layer
- Built using:
  - scikit-learn
  - NumPy
- Model used:
  - MLPRegressor (used as an autoencoder for anomaly detection)
- Detects unusual attacker behavior patterns

---

### 🧪 Data Generation Layer
- Custom synthetic data generator
- Key file:
  - `fake_environment_generator.py`
- Uses:
  - `random` module to simulate realistic system responses

---

### ⚙️ Orchestration Layer
- Central pipeline controller:
  - `project_runner.py`
- Connects all modules:
  - Data collection → processing → ML → output

---

## Tech Stack
- Python
- Cowrie Honeypot
- scikit-learn
- NumPy

---

## How It Works
1. Cowrie captures attacker activity
2. Logs are stored in `cowrie.json`
3. `log_reader.py` processes and extracts features
4. ML model analyzes behavior patterns
5. Anomalies are detected and flagged

---

## Project Structure

core/
┣ anomaly_detector.py
┣ log_reader.py
┗ fake_environment_generator.py

pipeline/
┗ project_runner.py

---

## My Contribution
- Designed and implemented anomaly detection pipeline
- Built log processing and feature extraction system
- Developed synthetic environment generator
- Integrated ML model for behavior analysis

---

## Future Improvements
- Real-time dashboard for monitoring attacks
- Advanced ML models for better accuracy
- Automated threat classification
- 
