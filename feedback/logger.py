import json
import os
from datetime import datetime
from core.models import LogEntry

class QualifAILogger:
    """
    Handles persistence of interaction logs to JSONL files.
    """
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
    def log(self, entry: LogEntry):
        """
        Appends a LogEntry to the daily log file.
        """
        filename = f"logs_{datetime.now().strftime('%Y-%m-%d')}.jsonl"
        filepath = os.path.join(self.log_dir, filename)
        
        with open(filepath, "a") as f:
            # We use .json() from Pydantic
            f.write(entry.model_dump_json() + "\n")
        
    def get_logs(self, date_str: str = None, days: int = 1) -> list:
        """
        Retrieves logs for a specific date or a rolling window of days.
        """
        if date_str:
            target_dates = [date_str]
        else:
            # Rolling window from today
            from datetime import timedelta
            end_date = datetime.now()
            target_dates = [(end_date - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(days)]
        
        all_logs = []
        for d in target_dates:
            filepath = os.path.join(self.log_dir, f"logs_{d}.jsonl")
            if os.path.exists(filepath):
                with open(filepath, "r") as f:
                    for line in f:
                        if line.strip():
                            all_logs.append(json.loads(line))
        return all_logs
