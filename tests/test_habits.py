def test_create_habit(client):
    r = client.post("/habits", json={"name": "Exercise", "description": "30 min"})
    assert r.status_code == 201
    body = r.json()
    assert body["name"] == "Exercise"
    assert body["is_active"] is True

def test_create_habit_blank_name(client):
    r = client.post("/habits", json={"name": "   "})
    assert r.status_code == 422

def test_list_habits(client, habit):
    r = client.get("/habits")
    assert r.status_code == 200
    assert any(h["id"] == habit["id"] for h in r.json())


def test_list_habits_includes_current_streak(client, habit):
    from datetime import date, timedelta

    today = date.today()
    for i in range(3):
        d = (today - timedelta(days=2 - i)).isoformat()
        client.post(f"/habits/{habit['id']}/checkins", json={"checked_in_on": d})

    body = client.get("/habits").json()
    matched = next(h for h in body if h["id"] == habit["id"])
    assert "current_streak" in matched
    assert matched["current_streak"] == 3


def test_list_habits_current_streak_zero_without_checkins(client, habit):
    body = client.get("/habits").json()
    matched = next(h for h in body if h["id"] == habit["id"])
    assert matched["current_streak"] == 0

def test_list_habits_active_only(client):
    active = client.post("/habits", json={"name": "Active"}).json()
    archived = client.post("/habits", json={"name": "Old"}).json()
    client.post(f"/habits/{archived['id']}/archive")

    r = client.get("/habits", params={"active_only": True})
    ids = [h["id"] for h in r.json()]
    assert active["id"] in ids
    assert archived["id"] not in ids

def test_get_habit(client, habit):
    r = client.get(f"/habits/{habit['id']}")
    assert r.status_code == 200
    assert r.json()["id"] == habit["id"]

def test_get_habit_not_found(client):
    assert client.get("/habits/9999").status_code == 404

def test_update_habit(client, habit):
    r = client.put(f"/habits/{habit['id']}", json={"name": "Meditate"})
    assert r.status_code == 200
    assert r.json()["name"] == "Meditate"

def test_archive_habit(client, habit):
    r = client.post(f"/habits/{habit['id']}/archive")
    assert r.status_code == 200
    assert r.json()["is_active"] is False
