import sys
import os
import json
from datetime import datetime

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from feedback.feedback_loop import FeedbackLoop
from core.brain import Brain

def test_auto_improve():
    print("Testing auto-improve functionality...")
    
    # 1. Create dummy logs to trigger heuristic
    os.makedirs("logs", exist_ok=True)
    log_file = f"logs/logs_{datetime.utcnow().strftime('%Y-%m-%d')}.jsonl"
    
    dummy_logs = []
    for i in range(10):
        dummy_logs.append({
            "timestamp": datetime.now().isoformat(),
            "lead_id": f"test-{i}",
            "action": "respond",
            "input_text": "Hello",
            "output_text": "Hi",
            "outcome": "Unqualified" if i < 5 else "Qualified"
        })
        
    with open(log_file, "w") as f:
        for log in dummy_logs:
            f.write(json.dumps(log) + "\n")
            
    loop = FeedbackLoop()
    brain = Brain()
    
    initial_prompt = brain.get_system_prompt()
    print("Initial prompt length:", len(initial_prompt))
    
    # 2. Run auto_improve
    result = loop.auto_improve()
    print(f"Auto-improve result: {result}")
    
    # 3. Verify brain.py was modified
    import importlib
    import core.brain
    importlib.reload(core.brain)
    from core.brain import Brain as ReloadedBrain
    
    new_brain = ReloadedBrain()
    new_prompt = new_brain.get_system_prompt()
    print("New prompt length:", len(new_prompt))
    
    assert len(new_prompt) > len(initial_prompt)
    assert "monthly budget" in new_prompt
    
    # 4. Check backup
    assert os.path.exists("/workspace/qualifai/core/brain.py.bak")
    
    # 5. Check changelog
    changelog_path = "/workspace/qualifai/logs/feedback_changelog.jsonl"
    assert os.path.exists(changelog_path)
    with open(changelog_path, "r") as f:
        changelog = [json.loads(line) for line in f]
    assert len(changelog) > 0
    print("Changelog entry:", changelog[-1])
    
    print("Test passed!")

if __name__ == "__main__":
    test_auto_improve()
