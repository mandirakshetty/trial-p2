import os
import random
from datetime import datetime

# Root directory
ROOT = r"E:/LogSpace"

# Regional hierarchy
structure = {
    "EMEA": {"Barclays": ["Unigy", "Pulse", "Touch"]},
    "Asia": {"SBI": ["Unigy", "Pulse", "Touch"]},
    "America": {"BankOfAmerica": ["Unigy", "Pulse", "Touch"]},
}

# Versions
versions = {
    "4.0": ["4.0.1"],
    "3.0": ["3.0.1"]
}

# Possible error codes
ERROR_CODES = [
    "E_INTERNAL_FAILURE",
    "E_NETWORK_DOWN",
    "E_TIMEOUT",
    "E_DB_FAIL",
    "E_API_UNAVAILABLE",
    "E_CONFIG_MISMATCH",
    "E_AUTH_FAILED",
    "E_FILE_NOT_FOUND"
]

# Components involved in logs
COMPONENTS = ["DataSync", "AuthService", "DBHandler", "LogIngestor", "Monitor", "APIClient"]

# Application-specific error patterns
APP_ERROR_PATTERNS = {
    "Unigy": [
        "Unigy trading endpoint failure",
        "Voice channel initialization error",
        "Unigy session manager crash"
    ],
    "Pulse": [
        "Pulse dashboard rendering stalled",
        "Pulse analytics computation timeout",
        "Pulse client connection dropped"
    ],
    "Touch": [
        "Touch UI communication error",
        "Touch gesture engine reported invalid state",
        "Touch service idle timeout"
    ]
}

# Info log patterns
INFO_PATTERNS = [
    "System running stable",
    "All components responsive",
    "Heartbeat received",
    "Background tasks running normally",
    "Scheduled job executed",
    "Configuration verified",
    "Startup sequence completed"
]


def random_timestamp():
    return datetime.utcnow().isoformat() + "Z"


def generate_error_log(app, count=8):
    """Generate multiple synthetic error log lines."""
    log_lines = []
    for _ in range(count):
        code = random.choice(ERROR_CODES)
        comp = random.choice(COMPONENTS)
        desc = random.choice(APP_ERROR_PATTERNS.get(app, ["Unknown failure"]))
        ts = random_timestamp()
        line = f"{ts} - ERROR - Component={comp} - Code: {code} - {desc}"
        log_lines.append(line)
    return "\n".join(log_lines)


def generate_info_log(app, count=6):
    """Generate multiple synthetic info log lines."""
    log_lines = []
    for _ in range(count):
        msg = random.choice(INFO_PATTERNS)
        ts = random_timestamp()
        line = f"{ts} - INFO - Application={app} - {msg}"
        log_lines.append(line)
    return "\n".join(log_lines)


def create_structure():
    for region, banks in structure.items():
        for bank, apps in banks.items():
            for app in apps:
                for version, subversions in versions.items():
                    for sub in subversions:

                        folder = os.path.join(ROOT, region, bank, app, version, sub)
                        os.makedirs(folder, exist_ok=True)

                        # File paths
                        error_file = os.path.join(folder, "logs.error")
                        info_file = os.path.join(folder, "logs.info")

                        # Generate content
                        error_content = generate_error_log(app)
                        info_content = generate_info_log(app)

                        # Write files
                        with open(error_file, "w", encoding="utf-8") as ef:
                            ef.write(error_content)

                        with open(info_file, "w", encoding="utf-8") as inf:
                            inf.write(info_content)

                        print(f"Created: {folder}")

    print("\nEnhanced LogSpace structure created successfully with randomized logs!")


if __name__ == "__main__":
    create_structure()
