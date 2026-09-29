from .logger import QualifAILogger
from typing import List, Dict
import collections
import json
import os
import shutil
from datetime import datetime

class FeedbackLoop:
    """
    Analyzes logs to provide insights and suggest prompt improvements.
    """
    def __init__(self):
        self.logger = QualifAILogger()

    def analyze_performance(self, days: int = 7) -> Dict:
        """
        Calculates basic metrics and generates improvement suggestions over a rolling window.
        """
        logs = self.logger.get_logs(days=days)
        if not logs:
            return {"status": f"No logs found for the last {days} days.", "suggestions": []}
            
        total_interactions = len(logs)
        outcomes = collections.Counter([log.get("outcome") for log in logs])
        
        analysis = {
            "period_days": days,
            "total_interactions": total_interactions,
            "outcome_breakdown": dict(outcomes),
            "suggestions": []
        }
        
        # Heuristics for actionable feedback
        unqual_rate = outcomes.get("Unqualified", 0) / max(total_interactions, 1)
        if unqual_rate > 0.4:
            analysis["suggestions"].append({
                "issue": "High Unqualification Rate",
                "action": "Add a budget qualification question earlier.",
                "prompt_diff": "IF lead budget is unknown after 2 messages, ASK: 'What is your monthly budget for consulting services?'"
            })
            
        qualifying_rate = outcomes.get("Qualifying", 0) / max(total_interactions, 1)
        if qualifying_rate > 0.6:
            analysis["suggestions"].append({
                "issue": "Leads stuck in Qualifying",
                "action": "Be more direct about booking the call.",
                "prompt_diff": "Be more direct: If they seem interested, suggest a specific time like 'tomorrow at 10 AM'."
            })
            
        return analysis

    def apply_suggestion(self, suggestion: Dict) -> bool:
        """
        Automatically applies a suggestion by modifying brain.py.
        """
        prompt_diff = suggestion.get("prompt_diff", "")
        if not prompt_diff:
            return False
            
        brain_path = "/workspace/qualifai/core/brain.py"
        backup_path = "/workspace/qualifai/core/brain.py.bak"
        
        try:
            # 1. Create backup
            shutil.copy2(brain_path, backup_path)
            
            # 2. Read and modify
            with open(brain_path, 'r') as f:
                lines = f.readlines()
            
            new_lines = []
            found_insertion_point = False
            
            for line in lines:
                new_lines.append(line)
                # Find the end of the instructions list to append
                if "ask follow-up questions one at a time." in line:
                    new_lines.append(f"6. {prompt_diff}\n")
                    found_insertion_point = True
            
            if not found_insertion_point:
                # Fallback: Find INSTRUCTIONS: header
                new_lines = []
                for line in lines:
                    new_lines.append(line)
                    if "INSTRUCTIONS:" in line:
                        new_lines.append(f"- {prompt_diff}\n")
                        found_insertion_point = True

            with open(brain_path, 'w') as f:
                f.writelines(new_lines)
            
            # 3. Log to changelog
            changelog_path = "/workspace/qualifai/logs/feedback_changelog.jsonl"
            os.makedirs(os.path.dirname(changelog_path), exist_ok=True)
            with open(changelog_path, 'a') as f:
                log_entry = {
                    "timestamp": datetime.now().isoformat(),
                    "suggestion": suggestion,
                    "status": "Applied"
                }
                f.write(json.dumps(log_entry) + "\n")
                
            return True
        except Exception as e:
            print(f"FeedbackLoop: Error applying suggestion: {e}")
            return False

    def auto_improve(self) -> str:
        """
        Analyzes performance and applies the first suggestion found.
        """
        analysis = self.analyze_performance()
        suggestions = analysis.get("suggestions", [])
        
        if not suggestions:
            return "No improvements needed at this time."
            
        success = self.apply_suggestion(suggestions[0])
        if success:
            return f"Successfully applied improvement: {suggestions[0]['issue']}"
        else:
            return f"Failed to apply improvement: {suggestions[0]['issue']}"

    def get_prompt_diff_report(self, days: int = 7) -> str:
        """
        Returns a formatted report of suggested prompt changes based on rolling window performance.
        """
        analysis = self.analyze_performance(days=days)
        if not analysis.get("suggestions"):
            return f"Current prompts are performing well over the last {days} days. No updates needed."
            
        report = f"--- ACTIONABLE PROMPT UPDATES ({days}-DAY WINDOW) ---\n"
        for sug in analysis["suggestions"]:
            report += f"\nISSUE: {sug['issue']}\n"
            report += f"ACTION: {sug['action']}\n"
            report += f"SUGGESTED DIFF:\n{sug['prompt_diff']}\n"
            report += "-" * 30 + "\n"
            
        return report
