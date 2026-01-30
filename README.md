# GitHub Webhook & Event Monitor

## 📌 Purpose
This project is a high-performance monitoring system designed to track real-time GitHub repository activities. It captures specific events—specifically **Push**, **Pull Request**, and **Merge** actions—using webhooks and processes them into a readable, time-sequenced interface. The goal is to provide developers with an automated audit log of repository changes without manual refreshes.

## 🛠 Technical Stack
- **Backend:** Node.js / Python (FastAPI) [Keep the one you used]
- **Frontend:** React.js / Next.js
- **Integration:** GitHub Webhooks API
- **Automation:** GitHub Actions (configured in `action-repo`)
- **Styling:** Tailwind CSS

## 🚀 Key Features & Implementation

### 1. Real-Time Webhook Integration
- Developed a robust endpoint to receive and validate payload signatures from GitHub.
- **Push Events:** Captures committer details, timestamps, and branch metadata.
- **Pull Request Events:** Monitors status changes (opened, synchronized).
- **Merge Events (Bonus):** Implemented logic to detect successful merges, providing a clear distinction between a standard PR and a completed code integration.

### 2. Intelligent Data Handling
- **Window-Based Refresh:** Implemented logic to prevent redundant data display. The system intelligently filters data that falls outside the active time window for the current refresh cycle.
- **Date Formatting:** Standardized ISO timestamps into a human-readable format, ensuring consistency across the UI regardless of the user's timezone.

### 3. High Readability & Code Standards
- **Clean Architecture:** Separated concerns between the webhook listener logic and the UI rendering.
- **Documentation:** Inline comments provided for complex asynchronous functions.
- **Variable Naming:** Followed industry-standard naming conventions for high maintainability.

## 📂 Repository Structure
- `webhook-repo`: Contains the core application logic, webhook server, and the frontend dashboard.
- `action-repo`: A secondary repository used to trigger dummy GitHub Actions for testing the integration.

## ⚙️ Installation & Setup
1. Clone the repository: `git clone [[your-repo-link]](https://github.com/kanakmegha/GithubWebhook.git)`
2. Install dependencies: `npm install` or `pip install -r requirements.txt`
3. Set your Webhook Secret in the `.env` file.
4. Run the development server: `npm run dev` or `uvicorn main:app --reload`

## 📝 Future Improvements
- Add persistent storage (PostgreSQL/MongoDB) for long-term event history.
- Implement Slack/Discord notifications for critical "Merge" events.
