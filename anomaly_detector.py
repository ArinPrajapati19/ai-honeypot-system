import datetime
import numpy as np
from sklearn.neural_network import MLPRegressor

from log_parser import load_logs, extract_features


def build_features(events):
    """
    Group events by IP address and calculate:
    [login_attempts, commands_entered, average_time_gap]
    """
    grouped = {}

    # Group events by IP
    for event in events:
        ip = event.get("ip")

        if not ip:
            continue

        if ip not in grouped:
            grouped[ip] = []

        grouped[ip].append(event)

    ip_features = {}

    # Build feature vector for each IP
    for ip, event_list in grouped.items():
        login_attempts = 0
        command_times = []

        for event in event_list:
            event_name = event.get("event", "")
            username = event.get("username")
            password = event.get("password")
            command = event.get("command")
            timestamp = event.get("timestamp")

            # Count login attempts
            if username or password or "login" in event_name.lower():
                login_attempts += 1

            # Count commands and store timestamps
            if command and timestamp:
                try:
                    # Example format:
                    # 2026-04-06T14:46:53.456387Z
                    dt = datetime.datetime.fromisoformat(
                        timestamp.replace("Z", "+00:00")
                    )
                    command_times.append(dt)
                except Exception:
                    pass

        commands_entered = len(command_times)

        # Calculate average time gap between commands
        average_time_gap = 0.0

        if commands_entered > 1:
            command_times.sort()

            gaps = []
            for i in range(1, len(command_times)):
                gap = (command_times[i] - command_times[i - 1]).total_seconds()
                gaps.append(gap)

            average_time_gap = sum(gaps) / len(gaps)

        ip_features[ip] = [
            login_attempts,
            commands_entered,
            average_time_gap
        ]

    return ip_features


def train_model():
    """
    Train a tiny neural-network autoencoder-like model
    on manually defined 'normal' behavior.
    """
    normal_examples = np.array([
        [1, 2, 10],
        [2, 3, 15],
        [1, 1, 20],
        [1, 0, 0],
        [2, 2, 12]
    ])

    model = MLPRegressor(
        hidden_layer_sizes=(4, 2, 4),
        max_iter=2000,
        random_state=42
    )

    # Train model to reconstruct the same input
    model.fit(normal_examples, normal_examples)

    return model


def detect_anomalies(ip_features, model):
    """
    Compare each IP feature vector against the model.
    Large reconstruction error = suspicious behavior.
    """
    threshold = 15.0

    for ip, features in ip_features.items():
        x = np.array([features])

        reconstructed = model.predict(x)

        # Mean Squared Error
        score = np.mean((x - reconstructed) ** 2)

        print(f"IP: {ip}")
        print(f"Features: {features}")
        print(f"Anomaly Score: {score:.2f}")

        if score > threshold:
            print("Status: Suspicious")
        else:
            print("Status: Normal")

        print("-" * 40)


def main():
    log_file = "var/log/cowrie/cowrie.json"

    try:
        raw_logs = load_logs(log_file)
    except FileNotFoundError:
        print(f"Could not find: {log_file}")
        return

    # Convert raw logs into simplified event dictionaries
    events = []
    for log in raw_logs:
        try:
            events.append(extract_features(log))
        except Exception:
            pass

    if not events:
        print("No events found.")
        return

    ip_features = build_features(events)

    if not ip_features:
        print("No usable IP features found.")
        return

    model = train_model()

    detect_anomalies(ip_features, model)


if __name__ == "__main__":
    main()
