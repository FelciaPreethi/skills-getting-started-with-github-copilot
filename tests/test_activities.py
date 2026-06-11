def test_get_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()

    assert "Chess Club" in data
    assert data["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_for_activity_adds_participant(client):
    response = client.post("/activities/Chess%20Club/signup?email=test@student.edu")

    assert response.status_code == 200
    assert response.json()["message"] == "Signed up test@student.edu for Chess Club"

    activity_response = client.get("/activities")
    assert "test@student.edu" in activity_response.json()["Chess Club"]["participants"]


def test_signup_duplicate_returns_bad_request(client):
    test_email = "duplicate@student.edu"

    first_response = client.post(f"/activities/Programming%20Class/signup?email={test_email}")
    assert first_response.status_code == 200

    second_response = client.post(f"/activities/Programming%20Class/signup?email={test_email}")
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student already signed up for this activity"


def test_signup_for_missing_activity_returns_not_found(client):
    response = client.post("/activities/NotAClub/signup?email=test@student.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant(client):
    participant_email = "michael@mergington.edu"
    response = client.delete(
        f"/activities/Chess%20Club/participants?email={participant_email}"
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {participant_email} from Chess Club"

    activity_response = client.get("/activities")
    assert participant_email not in activity_response.json()["Chess Club"]["participants"]


def test_remove_missing_participant_returns_not_found(client):
    response = client.delete(
        "/activities/Chess%20Club/participants?email=missing@student.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
