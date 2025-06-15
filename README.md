# 📈 Market Data Microservice

This is a production-ready microservice for polling, storing, and consuming financial market data using **FastAPI**, **Celery**, **Kafka**, **PostgreSQL**, and **Redis**. It supports real-time price ingestion and moving average computation for stock symbols.

---

## 🚀 Features

* ⎱ Poll price data via Celery workers using providers like Alpha Vantage or yFinance.
* 🧵 Stream price data through Kafka topics (`market.prices`).
* 🪮 Kafka consumers for:

  * Raw price ingestion
  * Moving average calculation
* 📦 Store and query data via PostgreSQL using SQLAlchemy ORM.
* ⟳ Background tasks and async architecture with Redis & Celery.
* 🔌 REST API using FastAPI with auto-generated OpenAPI docs.

---

## 💠 Tech Stack

* Python 3.12
* FastAPI
* Celery
* Kafka + Zookeeper
* PostgreSQL + SQLAlchemy
* Redis
* Docker & Docker Compose

---

## 📂 Project Structure

```
market-data-service/
│
├── app/
│   ├── api/                 # FastAPI routes
│   ├── core/                # Config, DB session
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   └── services/            # CRUD logic + Kafka consumers
│
├── worker.py                # Celery entrypoint
├── docker-compose.yml       # Multi-container setup
├── Dockerfile               # App Dockerfile
└── requirements.txt         # Python dependencies
```

---

## 📦 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/market-data-service.git
cd market-data-service
```

### 2. Configure Environment Variables

Create a `.env` file:

```bash
POSTGRES_USER=youruser
POSTGRES_PASSWORD=yourpass
POSTGRES_DB=marketdata
ALPHA_VANTAGE_API_KEY=your_api_key
```

### 3. Start all services with Docker Compose

```bash
docker-compose up --build
```

### 4. Visit the API

* FastAPI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📊 API Endpoints

| Method | Endpoint                     | Description                      |
| ------ | ---------------------------- | -------------------------------- |
| GET    | `/health`                    | Health check                     |
| POST   | `/prices/poll`               | Start polling prices for symbols |
| GET    | `/prices/latest?symbol=AAPL` | Get latest price for a symbol    |
| GET    | `/prices?symbol=AAPL`        | Get last 5 price points          |
| GET    | `/prices/status/{job_id}`    | Check Celery task status         |

---

## 🥪 Testing

Coming soon...

---

## 📄 License

MIT License. See `LICENSE` for details.
 
