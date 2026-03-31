🚀 AI Document Processing System
📌 Overview
This project is a full-stack document processing system that allows users to upload files, process them asynchronously, track progress in real-time, and manage results through a clean dashboard.

It demonstrates modern backend + frontend integration with asynchronous task handling using Celery and Redis.

🏗️ Architecture Overview
Frontend (React)
↓
FastAPI Backend (REST APIs)
↓
Celery Worker (Async Processing)
↓
Redis (Message Broker + Progress Tracking)
↓
SQLite Database

⚙️ Tech Stack
🔹 Backend
FastAPI

SQLite / PostgreSQL

SQLAlchemy

Celery

Redis

🔹 Frontend
React (Vite)

Axios

🚀 Features
📤 File Upload System

📊 Jobs Dashboard

🔄 Real-time Status Tracking (queued → processing → completed)

📄 Document Detail / Review Screen

✏️ Edit Workflow

✅ Finalize Workflow

🔁 Retry Failed Jobs

🗑️ Delete Single Record

🧹 Clear All History

📥 Export Data (JSON & CSV)

▶️ Setup Instructions
🔹 1. Clone Repository
git clone <YOUR_REPO_LINK>
cd ai-document-processing

🔹 2. Backend Setup
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

🔹 3. Start Redis
redis-server

🔹 4. Start Backend
uvicorn main --reload

🔹 5. Start Celery Worker
python -m celery -A celery_worker.celery worker --loglevel=info --pool=solo

🔹 6. Frontend Setup
cd frontend
npm install
npm run dev

▶️ Run Steps (Quick Start)
Start Redis

Start Backend

Start Celery Worker

Start Frontend

Open browser → http://localhost:5173

🧠 How It Works
User uploads a file

Backend stores file metadata in database

Celery processes the file asynchronously

Redis handles task queue and progress updates

Frontend fetches data every 2 seconds

User can view, edit, finalize, retry, or delete documents

⚠️ Assumptions
Files are processed using simulated logic

Local Redis server is used

Small file sizes are expected

Single user system (no authentication)

⚖️ Tradeoffs
Polling (every 2 seconds) used instead of WebSockets

SQLite used instead of production-grade DB

Simple UI used instead of heavy frameworks

🚫 Limitations
No authentication system

No cloud deployment (runs locally)

No file preview functionality

Not optimized for large-scale usage


📁 Sample Files
Folder:
sample_files/

Includes:

Sample PDF file

Sample image file

📤 Sample Outputs
Folder:
export_samples/

Includes:

JSON export file

CSV export file

🤖 AI Usage Disclosure
AI tools (ChatGPT) were used for:

Code structuring

Debugging

UI enhancement

Backend-frontend integration guidance

All logic implementation, testing, and understanding were done manually.

👩‍💻 Author
Priyanka 🚀
