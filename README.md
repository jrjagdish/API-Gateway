# 🚀 API Gateway Platform (FastAPI + Neon PostgreSQL)

A production-grade **API Gateway** that lets developers register, create projects, generate API keys, and proxy requests to external API providers through a single unified gateway.

This project is built to learn real backend engineering:
- Authentication  
- Project & API key management  
- Calling external APIs from a secure gateway  
- Clean modular architecture  
- FastAPI + SQLAlchemy best practices  

---

## 🎯 Purpose of This Project

Developers often work with many external APIs (weather, news, images, payments, AI, etc.).  
Managing different API keys, rate limits, retries, security, and routing becomes messy.

This API Gateway solves that by offering:

### ✔ One API key per project  
### ✔ Central routing to multiple external providers  
### ✔ Secure key storage (hashed)  
### ✔ Provider-level failover (upcoming)  
### ✔ Usage logging (upcoming)

Think of it as a small version of:  
**RapidAPI, Kong Gateway, Tyk API Gateway, or Google Apigee.**

---

## 🛠️ Tech Stack

- **FastAPI** (Backend framework)  
- **Neon PostgreSQL** (Cloud Postgres + SSL)  
- **SQLAlchemy ORM**  
- **HTTPX** for proxy requests  
- **JWT + bcrypt** for authentication  
- **Pydantic** for validation  
- **python-dotenv** for environment management  



## ⚙️ Environment Variables

Create a `.env` file:

DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DB?sslmode=require
JWT_SECRET=your_secret
JWT_ALGORITHM=HS256


---

## 🗄️ Database (Neon)

1. Create a free Neon Postgres project  
2. Copy the connection string  
3. Paste it in `.env`  
4. Backend auto-creates tables on startup  

---

## ▶️ Running the App

Install dependencies:

pip install -r requirements.txt


Run the server:



uvicorn app.main:app --reload


---

## 🚧 Features (MVP)

- User registration  
- User login (JWT)  
- Create projects  
- Generate API keys  
- Store keys hashed  
- Register providers  
- Proxy endpoint (upcoming)  
- Provider failover (upcoming)  
- Usage analytics (upcoming)  

---

## 🧠 Learning Outcome

- Real backend architecture  
- Database modeling  
- Authentication systems  
- API key lifecycle  
- Building scalable, modular services  
- Understanding how professional gateways work  
