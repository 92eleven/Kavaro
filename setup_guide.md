# QualifAI Client User Guide

Welcome to your new autonomous lead qualification system! QualifAI is designed to monitor your incoming leads, answer their questions, and book qualified appointments on your calendar without you lifting a finger.

## 🐳 Docker Quick Start (Recommended)
If you have Docker installed, this is the fastest way to get started.

1. **Setup Environment**: Copy `.env.example` to `.env` and fill in your API keys.
2. **Run System**: Execute `docker compose up -d`.
3. **Webhook Mode**: By default, the Docker container runs the webhook server on port `8080`.
4. **Logs**: Check performance with `docker compose logs -f`.
5. **Update Knowledge**: Edit `knowledge_base.json` and run `docker compose restart`.

## 🚀 Standard Getting Started

### 1. Configure Your "Brain"
The agent uses a file called `knowledge_base.json` to understand your business. You can open this file (it's just text) and update:
- **Qualification Criteria:** Tell the AI exactly who your ideal customer is.
- **FAQs:** Add common questions you get and the exact answers you want the AI to give.

### 2. Connect Your Accounts
Your agent needs permission to send emails and texts. These are stored in the `.env` file. You will need:
- **OpenAI API Key:** For the AI's reasoning.
- **Gmail App Password:** To send/receive emails.
- **Twilio Credentials:** To send/receive text messages.

### 3. Managing the Agent
Run the `run.py` application to see the control panel. From here, you can:
- **Sync Leads:** Click this to have the agent check for new messages and respond to them.
- **Analyze Feedback:** See how the agent is performing and view suggestions on how to improve its "sales scripts" (prompts).
- **View Configuration:** Verify your company name and booking link.

## 📈 Improving Performance
The agent tracks every conversation. If you notice it's qualifying the wrong people, go to the **Feedback Analysis** in the control panel. The AI will suggest specific "Prompt Diffs" (changes to its instructions) that you can apply to make it smarter over time.

## 🛡️ Security & Privacy
- All your API keys are stored locally on your server.
- The agent only responds to leads who contact you first.
- You can review every interaction in the `logs/` folder.

---
*For support or advanced customization, please contact your technical implementation team.*
