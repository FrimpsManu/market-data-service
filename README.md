# 📈 Market Data Microservice

A production-ready microservice for polling, storing, and consuming financial market data using **FastAPI**, **Kafka**, **Celery**, **PostgreSQL**, and **Redis**. It supports real-time price ingestion, task scheduling, and moving average calculations for stock symbols.

---

## 🚀 Features

- ✅ REST API with FastAPI  
- 🔁 Background polling with Celery  
- 📥 Kafka producer for price events  
- 🧮 Kafka consumer for 5-point moving average  
- 🗃️ PostgreSQL with SQLAlchemy ORM  
- 🧠 Redis for Celery backend  
- 🐳 Dockerized setup  

---

## 🧱 Tech Stack

- **Python 3.12**
- **FastAPI**
- **Celery**
- **Kafka + Zookeeper**
- **PostgreSQL + SQLAlchemy**
- **Redis**
- **Docker & Docker Compose**

---

## 📁 Project Structure

```
market-data-service/
│
├── app/
│   ├── api/                 # FastAPI routes
│   ├── core/                # Config & DB setup
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic request/response schemas
│   ├── services/            # Kafka consumers, CRUD
│   └── utils/               # Helper utilities (e.g., moving average)
│
├── tests/                   # Unit & integration tests
├── docker/                  # (Optional) container configs
├── Dockerfile               # FastAPI service Dockerfile
├── docker-compose.yml       # Orchestration of services
├── requirements.txt         # Python dependencies
├── worker.py                # Celery entrypoint
└── main.py                  # FastAPI entrypoint
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/FrimpsManu/market-data-service.git
cd market-data-service
```

### 2. Add environment variables

Create a `.env` file in the root directory:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=market_data
ALPHA_VANTAGE_API_KEY=your_api_key
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
```

> You can modify these values in `docker-compose.yml` or your own `.env`.

---

### 3. Run the app locally (Dockerized)

```bash
docker-compose up --build
```

- API docs: http://localhost:8000/docs
- Kafka topic: `market.prices`

---

## 📡 API Endpoints

| Method | Endpoint                       | Description                          |
|--------|-------------------------------|--------------------------------------|
| GET    | `/health`                     | Health check                         |
| GET    | `/prices/latest?symbol=AAPL`  | Get latest price for a stock symbol |
| GET    | `/prices?symbol=AAPL`         | Get last 5 price points              |
| GET    | `/prices/average?symbol=AAPL` | Get moving average                   |
| POST   | `/prices/poll`                | Start polling job via Celery         |
| GET    | `/prices/status/{job_id}`     | Get polling job status               |

---

## 🧪 Running Tests

Run unit tests with:

```bash
$env:PYTHONPATH = "."
pytest tests/
```

Make sure Docker services (especially Postgres) are running before testing API/database endpoints.

---

## 📦 Future Improvements

- Caching with Redis
- Rate limiting & error retry logic
- Postman collection

---

## 📄 License

MIT License
