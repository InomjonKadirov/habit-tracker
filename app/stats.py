from datetime import date, timedelta

def current_streak(checkin_dates: list[date], today: date) -> int:
    if not checkin_dates:
        return 0
    dates = sorted(set(checkin_dates), reverse=True)
    # Streak is still alive if last check-in was today or yesterday
    if dates[0] < today - timedelta(days=1):
        return 0
    expected = dates[0]
    streak = 0
    for d in dates:
        if d == expected:
            streak += 1
            expected -= timedelta(days=1)
        else:
            break
    return streak

def longest_streak(checkin_dates: list[date]) -> int:
    if not checkin_dates:
        return 0
    dates = sorted(set(checkin_dates))
    best = current = 1
    for i in range(1, len(dates)):
        if dates[i] == dates[i - 1] + timedelta(days=1):
            current += 1
            best = max(best, current)
        else:
            current = 1
    return best

def completion_rate_30d(checkin_dates: list[date], today: date) -> float:
    cutoff = today - timedelta(days=29)
    count = sum(1 for d in checkin_dates if cutoff <= d <= today)
    return round(count / 30 * 100, 1)
