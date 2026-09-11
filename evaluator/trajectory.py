import json
import time


class TrajectoryLogger:

    def __init__(self):
        self.events = []

    def log_event(self, action, details=None):

        event = {
            "timestamp": time.time(),
            "action": action,
            "details": details
        }

        self.events.append(event)

    def save(self, file_path):

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.events,
                file,
                indent=4
            )


if __name__ == "__main__":

    logger = TrajectoryLogger()

    logger.log_event(
        "task_started",
        {
            "task_id": "task_01"
        }
    )

    logger.log_event(
        "run_tests",
        {
            "command":
                "python -m pytest test_calculator.py"
        }
    )

    logger.log_event(
        "task_completed",
        {
            "passed": True
        }
    )

    logger.save(
        "results/trajectory_task_01.json"
    )

    print("Trajectory saved.")