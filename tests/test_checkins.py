from datetime import date, timedelta

def test_checkin_today(client, habit):
    r = client.post(f"/habits/{habit['id']}/checkins", json={})
    assert r.status_code == 201
    assert r.json()["habit_id"] == habit["id"]

def test_checkin_duplicate_same_day(client, habit):
    today = date.today().isoformat()
    client.post(f"/habits/{habit['id']}/checkins", json={"checked_in_on": today})
    r = client.post(f"/habits/{habit['id']}/checkins", json={"checked_in_on": today})
    assert r.status_code == 409

def test_checkin_specific_past_date(client, habit):
    past = (date.today() - timedelta(days=3)).isoformat()
    r = client.post(f"/habits/{habit['id']}/checkins", json={"checked_in_on": past})
    assert r.status_code == 201
    assert r.json()["checked_in_on"] == past

def test_delete_checkin(client, habit):
    r = client.post(f"/habits/{habit['id']}/checkins", json={})
    checkin_id = r.json()["id"]
    assert client.delete(f"/habits/{habit['id']}/checkins/{checkin_id}").status_code == 204
    checkins = client.get(f"/habits/{habit['id']}/checkins").json()
    assert not any(c["id"] == checkin_id for c in checkins)

def test_stats_no_checkins(client, habit):
    r = client.get(f"/habits/{habit['id']}/stats")
    assert r.status_code == 200
    body = r.json()
    assert body["current_streak"] == 0
    assert body["total_checkins"] == 0

def test_stats_streak_consecutive(client, habit):
    today = date.today()
    for i in range(3):
        d = (today - timedelta(days=2 - i)).isoformat()
        client.post(f"/habits/{habit['id']}/checkins", json={"checked_in_on": d})
    r = client.get(f"/habits/{habit['id']}/stats")
    assert r.json()["current_streak"] == 3
    assert r.json()["longest_streak"] == 3

def test_stats_streak_broken(client, habit):
    today = date.today()
    # Check in at today-4 and today-2 (gap at today-3, both too old to be current)
    for delta in [4, 2]:
        d = (today - timedelta(days=delta)).isoformat()
        client.post(f"/habits/{habit['id']}/checkins", json={"checked_in_on": d})
    r = client.get(f"/habits/{habit['id']}/stats")
    assert r.json()["current_streak"] == 0  # most recent is today-2, too old
    assert r.json()["longest_streak"] == 1  # today-4 and today-2 not consecutive

def test_stats_completion_rate(client, habit):
    today = date.today()
    for i in range(6):
        d = (today - timedelta(days=i)).isoformat()
        client.post(f"/habits/{habit['id']}/checkins", json={"checked_in_on": d})
    body = client.get(f"/habits/{habit['id']}/stats").json()
    assert body["completion_rate_30d"] == 20.0  # 6/30
