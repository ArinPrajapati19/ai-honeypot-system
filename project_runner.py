import json
from environment_generator import build_environment
from anomaly_detector import main as run_detector


def save_environment():
    env = build_environment()

    with open("generated_environment.json", "w") as f:
        json.dump(env, f, indent=2)

    print("Fake environment saved to generated_environment.json")


if __name__ == "__main__":
    print("Step 1: Generating fake environment...")
    save_environment()

    print("\nStep 2: Running anomaly detector...\n")
    run_detector()
