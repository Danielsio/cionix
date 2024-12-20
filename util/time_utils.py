def format_time(seconds):
    days = seconds // 86400  # 86400 seconds in a day
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60

    result = []
    if days > 0:
        result.append(f"ימים {days}")  # Hebrew for "days"
    if hours > 0:
        result.append(f"שעות {hours}")  # Hebrew for "hours"
    if minutes > 0:
        result.append(f"דקות {minutes}")  # Hebrew for "minutes"

    result.append(f"שניות {remaining_seconds}")  # Hebrew for "seconds"

    result.reverse()

    # Join the results with commas
    return ", ".join(result)

def format_time_dd_hh_mm_ss(seconds):
    """Format time in dd:hh:mm:ss."""
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60
    return f"{days:02}:{hours:02}:{minutes:02}:{remaining_seconds:02}"