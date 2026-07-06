from fastapi.testclient import TestClient

BOULDER = {"lat": 40.014986, "lon": -105.270546}
DENVER = {"lat": 39.739236, "lon": -104.984862}
SAN_FRANCISCO = {"lat": 37.7749, "lon": -122.4194}


def test_neighbors_happy_path(client: TestClient) -> None:
    response = client.post(
        "/v1/neighbors",
        json={
            "query_points": [BOULDER],
            "reference_points": [SAN_FRANCISCO, DENVER],
            "k": 1,
        },
    )
    assert response.status_code == 200
    body = response.json()
    match = body["results"][0]["neighbors"][0]
    assert match["reference_index"] == 1
    assert 23 < match["distance"] < 26
    assert body["query_count"] == 1
    assert body["reference_count"] == 2
    assert body["unit"] == "miles"
    assert body["elapsed_ms"] > 0


def test_invalid_coordinate_returns_422(client: TestClient) -> None:
    response = client.post(
        "/v1/neighbors",
        json={
            "query_points": [{"lat": 91.0, "lon": 0.0}],
            "reference_points": [DENVER],
        },
    )
    assert response.status_code == 422


def test_k_exceeding_reference_count_returns_422(client: TestClient) -> None:
    response = client.post(
        "/v1/neighbors",
        json={"query_points": [BOULDER], "reference_points": [DENVER], "k": 5},
    )
    assert response.status_code == 422


def test_over_point_limit_returns_413(client: TestClient) -> None:
    response = client.post(
        "/v1/neighbors",
        json={"query_points": [BOULDER] * 101, "reference_points": [DENVER]},
    )
    assert response.status_code == 413
    assert "limit per list is 100" in response.json()["detail"]


def test_liveness_probe(client: TestClient) -> None:
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readiness_probe_exercises_balltree(client: TestClient) -> None:
    response = client.get("/readyz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
