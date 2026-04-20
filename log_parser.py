import json

def load_logs(filepath):
    """
    Reads the log file line by line and parses valid JSON.
    Invalid JSON lines are ignored to prevent crashing.
    """
    logs = []
    try:
        # Open the file in read mode
        with open(filepath, 'r') as file:
            # Read line by line
            for line in file:
                try:
                    # Attempt to parse the line as JSON
                    log = json.loads(line)
                    logs.append(log)
                except json.JSONDecodeError:
                    # Ignore invalid JSON without crashing
                    continue
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
    
    return logs

def extract_features(log):
    """
    Extracts specific features from a single parsed log dictionary.
    Returns a new dictionary with the extracted fields.
    """
    extracted = {}
    
    # We use .get() to safely extract fields. 
    # If a field doesn't exist, it returns None.
    
    if "src_ip" in log:
        extracted["ip"] = log.get("src_ip")
        
    if "eventid" in log:
        extracted["event"] = log.get("eventid")
        
    if "timestamp" in log:
        extracted["timestamp"] = log.get("timestamp")
        
    if "username" in log:
        extracted["username"] = log.get("username")
        
    if "password" in log:
        extracted["password"] = log.get("password")
        
    if "input" in log:
        extracted["command"] = log.get("input")
        
    return extracted

def main():
    # The path to the cowrie JSON log file
    filepath = 'var/log/cowrie/cowrie.json'
    
    # 1. Read the file and parse all valid JSON lines
    raw_logs = load_logs(filepath)
    
    # 2. Extract features and store them in a list called `events`
    events = []
    for log in raw_logs:
        features = extract_features(log)
        # Avoid adding completely empty dictionaries
        if features: 
            events.append(features)
            
    # 3. Print the events clearly using json.dumps with indentation
    print(json.dumps(events, indent=2))

# Run the main function when the script is executed
if __name__ == "__main__":
    main()
