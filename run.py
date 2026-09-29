import sys
import os
from core.agent import QualifAIAgent
from feedback.feedback_loop import FeedbackLoop
from config import settings

def main():
    """
    Main entry point for the QualifAI management CLI.
    """
    # Check for auto-start server (useful for Docker)
    if os.environ.get("QUALIFAI_MODE") == "server":
        print(f"Starting QualifAI in server mode...")
        import server
        server.start_server()
        return

    print(f"--- Welcome to {settings.APP_NAME} Control Panel ---")
    
    # Check for .env
    if not os.path.exists(".env"):
        print("WARNING: .env file not found. System may not function correctly.")
        
    agent = QualifAIAgent()
    loop = FeedbackLoop()
    
    while True:
        print("\nMain Menu:")
        print("1. Process New Leads (Sync Integrations)")
        print("2. Run Feedback Analysis (View Prompt Diffs)")
        print("3. Auto-Improve System (Analyze & Apply)")
        print("4. View System Configuration")
        print("5. Start Webhook Server (Port 8080)")
        print("6. Exit")
        
        try:
            choice = input("\nEnter choice (1-6): ")
        except EOFError:
            break
            
        if choice == "1":
            print("\nConnecting to Gmail and Twilio...")
            agent.process_new_leads()
            print("Sync complete.")
        elif choice == "2":
            print("\nAnalyzing interaction logs...")
            report = loop.get_prompt_diff_report()
            print(report)
        elif choice == "3":
            print("\nAuto-improving prompts based on log analysis...")
            result = loop.auto_improve()
            print(result)
        elif choice == "4":
            print(f"\n--- {settings.COMPANY_NAME} CONFIG ---")
            print(f"Model: {settings.MODEL_NAME}")
            print(f"Booking Link: {settings.BOOKING_LINK}")
            print("\nCurrent System Prompt:")
            print(agent.brain.get_system_prompt())
        elif choice == "5":
            print(f"\nStarting Webhook Server on {settings.WEBHOOK_HOST}:{settings.WEBHOOK_PORT}...")
            import threading
            import server
            import uvicorn
            # Share the existing agent with the server
            server._agent = agent
            thread = threading.Thread(
                target=uvicorn.run, 
                args=(server.app,), 
                kwargs={"host": settings.WEBHOOK_HOST, "port": settings.WEBHOOK_PORT},
                daemon=True
            )
            thread.start()
            print("Webhook server is running in the background.")
        elif choice == "6":
            print("Shutting down...")
            sys.exit()
        else:
            print("Invalid selection.")

if __name__ == "__main__":
    main()
