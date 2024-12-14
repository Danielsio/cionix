def format_time(seconds):
    days = seconds // 86400  # 86400 seconds in a day
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60

    result = []
    if days > 0:
        result.append(f"{days} day(s)")
    if hours > 0:
        result.append(f"{hours} hour(s)")
    if minutes > 0:
        result.append(f"{minutes} minute(s)")
    result.append(f"{remaining_seconds} second(s)")

    return ", ".join(result)
