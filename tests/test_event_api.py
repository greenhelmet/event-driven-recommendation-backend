import pytest


def test_create_event_success(client, api_prefix):
    """
    이벤트 생성 성공 케이스
    """
    payload = {
        "user_id": 123,
        "item_id": "item_456",
        "event_type": "click",
    }

    response = client.post(
        f"{api_prefix}/events",
        json=payload,
    )

    assert response.status_code == 201

    body = response.json()
    assert body["user_id"] == 123
    assert body["item_id"] == "item_456"
    assert body["event_type"] == "click"
    assert "id" in body
    assert "created_at" in body


def test_create_event_validation_error(client, api_prefix):
    """
    요청 스키마 검증 실패 (422)
    """
    payload = {
        # user_id 누락
        "event_type": "click",
    }

    response = client.post(
        f"{api_prefix}/events",
        json=payload,
    )

    assert response.status_code == 422

    body = response.json()
    assert body["code"] == "VALIDATION_ERROR"
    assert body["message"] == "Invalid request"
    assert "detail" in body


@pytest.mark.xfail(reason="GET /events/{id} endpoint not implemented yet")
def test_get_event_not_found(client, api_prefix):
    """
    존재하지 않는 이벤트 조회
    """
    response = client.get(f"{api_prefix}/events/1")

    assert response.status_code == 400

    body = response.json()
    assert body["code"] == "EVENT_NOT_FOUND"
    assert body["message"] == "Event not found"
    assert body["detail"]["event_id"] == 1


@pytest.mark.xfail(reason="GET /events/{id} endpoint not implemented yet")
def test_get_event_success(client, api_prefix):
    """
    이벤트 단건 조회 성공
    """
    create_payload = {
        "user_id": 456,
        "item_id": "item_789",
        "event_type": "view",
    }

    create_response = client.post(
        f"{api_prefix}/events",
        json=create_payload,
    )

    assert create_response.status_code == 201
    event_id = create_response.json()["id"]

    response = client.get(f"{api_prefix}/events/{event_id}")

    assert response.status_code == 200

    body = response.json()
    assert body["id"] == event_id
    assert body["user_id"] == 456
    assert body["item_id"] == "item_789"
    assert body["event_type"] == "view"
