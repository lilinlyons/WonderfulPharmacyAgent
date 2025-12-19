# Wonderful Pharmacy Agent - Setup & Launch Guide

A full-stack pharmacy chatbot application with BERT-based intent classification, powered by OpenAI's API.
To see a breakdown of the Tools/utils and APIs look at the README.md in the backend directory.
## Prerequisites

- **Node.js** 22+ (for frontend)
- **Python** 3.10+ (for backend)
- **Docker & Docker Compose** (optional, for containerized deployment)
- **OpenAI API Key** (get one at https://platform.openai.com)

---

## Project Structure

```
project-root/
├── backend/
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── requirements.txt
│   ├── app.py
│   ├── agents/
│   ├── bert/
│   │   ├── classifier.py
│   │   ├── model.py
│   │   ├── model_out/          (BERT model - not in Docker)
│   │   └── inference_model/
│   └── __pycache__/
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── src/
│   └── public/
├── docker-compose.yml
├── .env                        (create this file)
└── .gitignore
```

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd wonderful-pharmacy-agent
```

### 2. Create Environment File

Create a `.env` file in the project root:

```bash
touch .env
```

Add your OpenAI API key:

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

**⚠️ Important:** Add `.env` to `.gitignore` to avoid committing secrets.

```bash
echo ".env" >> .gitignore
```

### 4. Download pre-trained BERT Model
## ⚠️ IMPORTANT – REQUIRED BEFORE YOU START

Before running **anything**, you **must download the BERT model files**.

### Download the BERT Model ZIP

Download the ZIP file from Google Drive:

**https://drive.google.com/file/d/1azqrJSCV6cYigKUUkzWTNNZWcNWQcnco/view?usp=drive_link**

### Extract & Place the Folder

1. Unzip the downloaded file  
2. You will get a folder named: bert
3. Move it into the backend folder so the structure looks like:
project-root/
├── backend/
│   ├── bert/
│   ├── requirements.txt
│   ├── app.py
|   └── ...


---

## Option 1: Docker Compose (Recommended)

### Launch with Docker
Change directory into the project root (with the Dockerfile) and run:
```bash
docker-compose up --build
```

This will:
- Build the backend image (Python + dependencies)
- Pull the frontend image (Node 22 Alpine)
- Start both services with proper networking
- Mount your local directories for development

### Access the App

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000

### Useful Docker Commands

```bash
# View logs
docker-compose logs -f

# View backend logs only
docker-compose logs -f backend

# Stop services
docker-compose down

# Rebuild without cache
docker-compose up --build --no-cache

# Remove volumes
docker-compose down -v

# Run a one-off command in backend
docker-compose exec backend python -c "import torch; print(torch.cuda.is_available())"
```

### Troubleshooting Docker

**Issue: "no space left on device"**
```bash
docker system prune -a
docker-compose up --build
```

**Issue: Model files not mounting**
Ensure `.dockerignore` is in the `backend/` directory and contains:
```
bert/model_out
__pycache__
*.pyc
.git
.env
```

---

## Option 2: Manual Setup (Local Development)

### Backend Setup

#### 1. Create Python Virtual Environment

```bash
cd backend
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

#### 2. a) Install Dependencies

```bash
pip install -r requirements.txt
```
#### 2. b) Initiate DB

```bash
cd backend
python utils/db/seed.py
```

#### 3. Ensure BERT Model Files Exist

Make sure your trained BERT model is at:
```
backend/bert/model_out/
```

If not, download or train your model first.

#### 4. Start Backend Server

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

The backend will start at `http://localhost:8000`

### Frontend Setup

#### 1. Install Dependencies

```bash
cd frontend
npm install
```

#### 2. Start Development Server

```bash
npm run dev
```

The frontend will start at `http://localhost:5173`

---

## Environment Variables

### Backend (.env)

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | ✅ Yes | Your OpenAI API key for GPT models |

## Development Workflow

### With Docker Compose (Recommended)

```bash
# Start services in watch mode
docker-compose up

# In another terminal, make code changes
# Both frontend and backend will auto-reload

# View changes at http://localhost:5173
```

### Manual Setup

#### Terminal 1 (Backend)
```bash
cd backend
source venv/bin/activate
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

#### Terminal 2 (Frontend)
```bash
cd frontend
npm run dev
```

---

## API Documentation

Look in backend/README.md for full API docs.

## Troubleshooting


**Issue: Port already in use**

```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>
```

## Performance Tips

- **BERT Model Caching:** The BERT model is loaded once at startup and reused
- **Volume Mounting:** Using Docker volumes avoids copying heavy model files
- **Hot Reload:** Both services support hot reload for faster development

---

## Next Steps

1. Train or fine-tune your BERT model
2. Update intent categories in `backend/bert/classifier.py`
3. Customize the UI in `frontend/src/`
4. Deploy to production (AWS, GCP, Azure, etc.)

---

## Support

For issues or questions:
1. Check logs: `docker-compose logs -f`
2. Verify `.env` file is set up correctly
3. Ensure all prerequisites are installed
4. Check that ports 8000 and 5173 are available
