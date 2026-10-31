from app.analytics import (
    get_total_revenue,
    get_top_product,
    get_region_sales,
    get_monthly_sales,
    analyze_sales
)

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_total_revenue():
    result = get_total_revenue()
    assert result == 1439200


def test_top_product():
    result = get_top_product()
    assert result["product"] == "Monitor"


def test_region_sales():
    result = get_region_sales()

    assert len(result) > 0
    assert result[0]["region"] == "South"


def test_monthly_sales():
    result = get_monthly_sales()

    assert len(result) == 6
    assert all(item["revenue"] > 0 for item in result)


def test_invalid_metric():
    try:
        analyze_sales(metric="invalid")
        assert False, "Expected ValueError"
    except ValueError:
        assert True

def test_empty_question():
    response = client.post(
        "/ask",
        json={"question": ""}
    )

    assert response.status_code == 400


def test_missing_question():
    response = client.post(
        "/ask",
        json={}
    )