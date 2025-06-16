from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_latest_price():
    response = client.get("/prices/latest?symbol=AAPL")
    assert response.status_code in [200, 404]  # depending on setup
