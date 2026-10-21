import os

def get_pass_threshold() -> float:
    return float(os.getenv("PASS_THRESHOLD", "60.0"))