from fastapi.testclient import TestClient


def test_create_document(client: TestClient) -> None:
    payload = {"title": "policy", "language": "ar", "content": "نص"}

    response = client.post("/api/v1/documents", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert "id" in body
    assert body["title"] == payload["title"]


def test_get_missing_document_returns_404(client: TestClient) -> None:
    response = client.get("api/v1/document/9999")
    assert response.status_code == 404


def test_create_rejects_invalid_language(client: TestClient) -> None:
    payload = {"title": "policy", "language": "fr", "content": "نص"}
    response = client.post("/api/v1/documents", json=payload)
    assert response.status_code == 422


def test_delete_document(client: TestClient) -> None:
    created = client.post(
        "/api/v1/documents", json={"title": "x", "language": "en", "content": "y"}
    )
    doc_id = created.json()["id"]

    response = client.delete(f"/api/v1/documents/{doc_id}")

    assert response.status_code == 204
    assert client.get(f"api/v1/documents/{doc_id}").status_code == 404
