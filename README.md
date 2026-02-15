# 🚀 SMB02 Outreach Engine

**Production-Ready AI Outreach System with Subscription Plans**

A terminal-first, scalable, modular FastAPI-based AI Outreach Engine that generates personalized cold emails using BitNet AI model. Features multi-tier subscription management, MongoDB authentication, and file-based memory storage.

## ✨ Features

- 🤖 **AI-Powered**: BitNet model for intelligent email generation
- 📊 **Subscription Tiers**: FREE, PRO, ULTRA, BUSINESS with daily quotas
- 🔐 **Secure**: JWT authentication + bcrypt password hashing
- 📈 **Scalable**: Production-ready FastAPI architecture
- 💾 **File-Based Memory**: Local JSON chat storage (NO MongoDB for memory)
- 🎨 **Modern UI**: ChatGPT-like interface with dark theme
- 🐳 **Docker Ready**: Docker & Docker Compose support
- 📱 **Terminal-First**: CLI tool for easy management
- 💬 **Multi-Language**: Supports any language for outreach

## 📋 Table of Contents

- [Architecture](#architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Subscription Plans](#subscription-plans)
- [Development](#development)
- [Deployment](#deployment)

## 🏗️ Architecture

### Technology Stack

| Component | Technology |
|-----------|------------|
| Backend | FastAPI (Python 3.11) |
| Frontend | HTML + CSS + JavaScript (Jinja2) |
| Database | MongoDB (Auth + Quotas only) |
| Memory | Local JSON files |
| AI Model | BitNet (Hugging Face) |
| Authentication | JWT + bcrypt |
| Containerization | Docker & Docker Compose |

### Directory Structure

```
smb02_outreach_engine/
│
├── app/
│   ├── main.py                 # FastAPI app entry
│   ├── config.py               # Configuration
│   ├── dependencies.py         # Dependency injection
│   │
│   ├── middleware/
│   │   └── rate_limiter.py     # Quota enforcement
│   │
│   ├── routes/
│   │   ├── auth.py             # Authentication
│   │   ├── chat.py             # Chat endpoints
│   │   ├── history.py          # Chat history
│   │   ├── linkedin.py         # LinkedIn analysis (placeholder)
│   │   └── billing.py          # Billing & quotas
│   │
│   ├── services/
│   │   ├── bitnet_loader.py    # Model loading
│   │   ├── memory_service.py   # Chat memory
│   │   ├── mail_generator.py   # Email generation
│   │   ├── apify_service.py    # LinkedIn API (placeholder)
│   │   └── subscription_service.py  # Subscription logic
│   │
│   ├── models/
│   │   └── user_model.py       # Pydantic schemas
│   │
│   ├── templates/
│   │   ├── layout.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── chat.html
│   │   ├── pricing.html
│   │   └── docs.html
│   │
│   └── static/
│       ├── style.css
│       └── chat.js
│
├── models_cache/               # BitNet model cache
├── memory/                     # User chat memory (JSON)
├── .env.example               # Environment template
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Container image
├── docker-compose.yml         # Multi-container setup
├── cli.py                     # CLI tool
└── README.md                  # Documentation
```

## 🚀 Installation

### Prerequisites

- Python 3.11+
- MongoDB 5.0+
- Docker (optional)
- Git

### Option 1: Manual Installation

```bash
# Clone repository
git clone https://github.com/rahulkate173/Outreach-Engine-.git
cd Outreach-Engine-

# Create virtual environment
python -m venv venv

# Activate venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your settings

# Create directories
mkdir -p models_cache memory
```

### Option 2: Docker Installation

```bash
# Clone repository
git clone https://github.com/rahulkate173/Outreach-Engine-.git
cd Outreach-Engine-

# Build and start
docker-compose up -d

# Check logs
docker-compose logs -f fastapi
```

### Option 3: EXE (Windows)

```bash
# Build executable
pyinstaller --onefile cli.py

# Run
dist/cli.exe auth start
```

## 📖 Quick Start

### Using CLI

```bash
# Start with auth flow
python cli.py auth

# OR start server directly
python cli.py server

# Reset model cache
python cli.py reset-model

# Docker commands
python cli.py docker-up
python cli.py docker-down
```

### Using Direct Python

```bash
# Start FastAPI
python -m uvicorn app.main:app --reload

# Server runs on: http://localhost:8000
```

### Using Docker Compose

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f
```

## ⚙️ Configuration

### Environment Variables (.env)

```env
# FastAPI
FASTAPI_ENV=development
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# MongoDB
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=smb02_db
MONGODB_USER=root
MONGODB_PASSWORD=password

# Hugging Face
HF_TOKEN=your-huggingface-token
MODEL_NAME=QuantFactory/BitNet-3B-1.58-nf4
MODEL_CACHE_DIR=./models_cache

# Paths
MEMORY_DIR=./memory
API_PORT=8000

# Credentials
APIFY_API_TOKEN=your-apify-token
```

### MongoDB Setup

```bash
# Using Docker
docker run -d \
  -e MONGO_INITDB_ROOT_USERNAME=root \
  -e MONGO_INITDB_ROOT_PASSWORD=password \
  -p 27017:27017 \
  mongo:latest

# OR use MongoDB Atlas
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/smb02_db
```

## 📡 API Documentation

### Authentication

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "email": "user@example.com",
    "plan": "FREE",
    "daily_requests": 0,
    "created_at": "2024-02-15T10:30:00"
  }
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password"
}
```

### Chat

#### Send Message
```http
POST /api/chat/message
Authorization: Bearer {token}
Content-Type: application/json

{
  "chat_id": "550e8400-e29b-41d4-a716-446655440000",
  "content": "Generate email for this person...",
  "recipient_name": "John Doe",
  "company": "Tech Corp",
  "job_title": "CTO"
}
```

**Response:**
```json
{
  "chat_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Generated response with email...",
  "generated_mail": {
    "subject": "Quick question about Tech Corp 👋",
    "body": "Hi John...",
    "preview": "Quick question...",
    "personalization_score": 0.85
  },
  "quota_remaining": 2
}
```

#### Create New Chat
```http
POST /api/chat/create-chat
Authorization: Bearer {token}
```

### History

#### List Chats
```http
GET /api/history/chats
Authorization: Bearer {token}
```

#### Get Chat
```http
GET /api/history/chat/{chat_id}
Authorization: Bearer {token}
```

#### Delete Chat
```http
DELETE /api/history/chat/{chat_id}
Authorization: Bearer {token}
```

### Billing

#### Get Quota Status
```http
GET /api/billing/quota
Authorization: Bearer {token}
```

**Response:**
```json
{
  "plan": "FREE",
  "daily_limit": 3,
  "daily_requests": 2,
  "remaining": 1,
  "quota_exceeded": false
}
```

#### Get Plans
```http
GET /api/billing/plans
```

#### Upgrade Plan
```http
POST /api/billing/upgrade
Authorization: Bearer {token}
Content-Type: application/json

{
  "new_plan": "PRO"
}
```

## 💰 Subscription Plans

| Plan | Daily Limit | Price | Features |
|------|-------------|-------|----------|
| **FREE** | 3 | $0/mo | Basic features, community support |
| **PRO** | 200 | $29/mo | Advanced analytics, email support |
| **ULTRA** | 1,000 | $99/mo | Priority support, custom workflows |
| **BUSINESS** | ∞ | Custom | Unlimited, dedicated support, API |

### Daily Quota Enforcement

- ✅ Quota reset at midnight (00:00 UTC)
- ✅ Real-time quota checking
- ✅ Automatic plan downgrades (optional)
- ✅ Quota alerts at 80%, 95%, 100%

## 📝 Frontend Usage

### Login/Register
- Navigate to `http://localhost:8000`
- Register with email and password
- Default plan: FREE (3 requests/day)

### Chat Interface
- Left sidebar: Conversation history
- Main area: Chat messages
- Plan badge: Shows current plan
- Quota display: Remaining requests today

### Input Fields
1. **Recipient Name** - Person's name for personalization
2. **Company** - Target company name
3. **Job Title** - Person's role
4. **Message** - Context for email generation

### Pricing Page
- View all subscription plans
- Upgrade to PRO/ULTRA/BUSINESS
- See feature comparison

## 🔧 Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest -v

# With coverage
pytest --cov=app
```

### Database Migrations

```bash
# Check MongoDB collections
mongo --eval "db.getMongo().getDBNames()"

# Create indexes (auto-created)
# No manual migrations needed
```

### Model Management

```bash
# View cached model
ls -la models_cache/

# Clear cache
python cli.py reset-model

# Download latest BitNet
HF_TOKEN=your_token python -c "from transformers import AutoModel; AutoModel.from_pretrained('QuantFactory/BitNet-3B-1.58-nf4')"
```

## 📦 Deployment

### Production Checklist

- [ ] Generate new `SECRET_KEY`
- [ ] Set `FASTAPI_ENV=production`
- [ ] Configure MongoDB with authentication
- [ ] Set up HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Set resource limits in Docker
- [ ] Enable monitoring & logging
- [ ] Backup MongoDB regularly

### Heroku Deployment

```bash
# Create app
heroku create smb02-outreach

# Add MongoDB add-on
heroku addons:create mongolab:sandbox

# Deploy
git push heroku main

# View logs
heroku logs -t
```

### AWS EC2 Deployment

```bash
# SSH into instance
ssh -i key.pem ubuntu@instance-ip

# Clone and setup
git clone https://github.com/rahulkate173/Outreach-Engine-.git
cd Outreach-Engine-

# Install Docker
sudo apt install docker.io docker-compose

# Start services
docker-compose up -d

# Setup nginx reverse proxy
sudo apt install nginx
```

### Digital Ocean App Platform

```bash
# Push to GitHub
git push origin main

# Connect to App Platform
# - Link GitHub repo
# - Set environment variables
# - Deploy
```

## 🔒 Security

- ✅ JWT token authentication
- ✅ bcrypt password hashing (10 rounds)
- ✅ CORS middleware
- ✅ SQL injection protection (MongoDB parameterized)
- ✅ Rate limiting per user
- ✅ Environment secrets management
- ✅ HTTPS enforced in production

## 📊 Monitoring

### Logs
```bash
# Application logs
docker-compose logs -f fastapi

# MongoDB logs
docker-compose logs -f mongodb
```

### Metrics
```bash
# Health check endpoint
curl http://localhost:8000/health

# API performance
curl http://localhost:8000/api/billing/quota \
  -H "Authorization: Bearer {token}"
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 💬 Support

- 📧 Email: support@smb02.io
- 💬 Discord: [Join Community](https://discord.gg/smb02)
- 📖 Documentation: [Docs](http://localhost:8000/docs)
- 🐛 Issues: [GitHub Issues](https://github.com/rahulkate173/Outreach-Engine-/issues)

## 🎯 Roadmap

- [ ] WebSocket support for real-time chat
- [ ] Advanced NLP for email personalization
- [ ] Multi-language support
- [ ] Integration with email services (Gmail, Outlook)
- [ ] Analytics dashboard
- [ ] Team collaboration features
- [ ] Custom AI model training
- [ ] Mobile app (React Native)
- [ ] Slack integration
- [ ] Zapier integration

## 🙏 Acknowledgments

- BitNet team at Hugging Face
- FastAPI framework
- MongoDB community
- All contributors

---

**Made with ❤️ by SMB02 Team**

**Live Demo:** https://smb02-outreach.herokuapp.com  
**GitHub:** https://github.com/rahulkate173/Outreach-Engine-  
**Documentation:** https://smb02-outreach.io/docs