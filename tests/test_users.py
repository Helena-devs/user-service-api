def test_create_user(client, auth_headers):
    response = client.post(
        "/api/v1/users",
        json={
            "email": "john@example.com",
            "full_name": "John Doe",
            "password": "securepassword",
        },
        headers=auth_headers,
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "john@example.com"
    assert data["full_name"] == "John Doe"
    assert data["is_active"] is True
    assert "id" in data
    assert "password" not in data


def test_get_user_by_id(client, auth_headers):
    create_response = client.post(
        "/api/v1/users",
        json={
            "email": "jane@example.com",
            "full_name": "Jane Doe",
            "password": "securepassword",
        },
        headers=auth_headers,
    )
    user_id = create_response.json()["id"]

    response = client.get(f"/api/v1/users/{user_id}", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["email"] == "jane@example.com"


def test_list_users(client, auth_headers):
    client.post(
        "/api/v1/users",
        json={
            "email": "list@example.com",
            "full_name": "List User",
            "password": "securepassword",
        },
        headers=auth_headers,
    )

    response = client.get("/api/v1/users", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert len(data["items"]) >= 1
