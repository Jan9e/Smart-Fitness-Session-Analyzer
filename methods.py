def compute_summaries(session):
    if session.valid_count == 0:
        return {
            "valid_count": 0,
            "rejected_count": session.rejected_count,
            "total_count": session.total_count,
            "average_heart_rate": None,
            "min_heart_rate": None,
            "max_heart_rate": None,
            "average_activity": None,
            "min_activity": None,
            "average_skin_response": None,
            "average_signal_quality": None
        }

    hrs = [o.heart_rate for o in session.valid_observations]
    acts = [o.activity_level for o in session.valid_observations]
    skins = [o.skin_response for o in session.valid_observations]
    temps = [o.temperature for o in session.valid_observations]
    quals = [o.signal_quality for o in session.valid_observations]

    return {
        "valid_count": session.valid_count,
        "rejected_count": session.rejected_count,
        "total_count": session.total_count,
        "average_heart_rate": sum(hrs)/len(hrs),
        "min_heart_rate": min(hrs),
        "max_heart_rate": max(hrs),
        "average_activity": sum(acts)/len(acts),
        "min_activity": min(acts),
        "max_activity": max(acts),
        "average_skin_response": sum(skins)/len(skins),
        "average_temperature": sum(temps)/len(temps),
        "average_signal_quality": sum(quals)/len(quals)
    }

def detect_recovery(session):
    if session.valid_count < 6:
        return False

    obs = session.valid_observations
    n = len(obs)
    first_third = obs[: n // 3]
    last_third = obs[-n // 3:]

    avg_hr_first = sum(o.heart_rate for o in first_third) / len(first_third)
    avg_hr_last = sum(o.heart_rate for o in last_third) / len(last_third)
    avg_act_first = sum(o.activity_level for o in first_third) / len(first_third)
    avg_act_last = sum(o.activity_level for o in last_third) / len(last_third)

    baseline_hr = session.participant.baseline_heart_rate

    started_active = avg_hr_first > baseline_hr + 20
    hr_dropped = avg_hr_last < avg_hr_first - 15       # ← fixed
    activity_dropped = avg_act_last < avg_act_first - 0.2

    return started_active and hr_dropped and activity_dropped

def classify_session(session, summaries):
    if session.valid_count < 3:
        return "insufficient data", "fewer than 3 valid observations"

    if detect_recovery(session):
        return "recovering", ("heart rate and activity declined near the end of the session")

    baseline_hr = session.participant.baseline_heart_rate
    avg_hr = summaries["average_heart_rate"]
    avg_act = summaries["average_activity"]

    if avg_act < 0.25 and avg_hr < baseline_hr  + 10:
        return "resting", (
            f"low activity ({avg_act:.2f}) and heart rate near baseline "
            f"({avg_hr:.0f} vs {baseline_hr} bpm)"
        )

    if avg_act > 0.65 and avg_hr > baseline_hr + 40:
        return "high activity", (
            f"high activity ({avg_act:.2f}) or heart rate well above baseline "
            f"({avg_hr:.0f} vd {baseline_hr} bpm)"
        )

    return "moderate activity", (
        f"moderate activity ({avg_act:.2f}) and heart rate above baseline "
        f"({avg_hr:.0f} vs {baseline_hr} bpm)" 
    )

def format_report(report):
    session = report.session
    summaries = report.summaries
    p = session.participant

    lines = []
    lines.append(f"=== Session report for participant {p.participant_id} ===")
    lines.append(f"Baseline heart rate: {p.baseline_heart_rate} bpm")
    lines.append(f"Baseline skin response: {p.baseline_skin_response}")
    lines.append(f"Baseline temperature: {p.baseline_temperature} °C")
    lines.append("")
    lines.append(f"Total observations: {summaries['total_count']}")
    lines.append(f"Valid observations: {summaries['valid_count']}")
    lines.append(f"Rejected observations: {summaries['rejected_count']}")
    lines.append("")

    if summaries["valid_count"] == 0:
        lines.append("No valid observations to summarise.")
    else:
        lines.append(
            f"Average heart rate: {summaries['average_heart_rate']:.1f} bpm "
            f"(min {summaries['min_heart_rate']}, max {summaries['max_heart_rate']})"
        )
        lines.append(
            f"Average activity level: {summaries['average_activity']:.2f} "
            f"(min {summaries['min_activity']:.2f}, max {summaries['max_activity']:.2f})"
        )
        lines.append(f"Average skin response: {summaries['average_skin_response']:.2f}")
        lines.append(f"Average temperature: {summaries['average_temperature']:.2f} °C")
        lines.append(f"Average signal quality: {summaries['average_signal_quality']:.2f}")

    lines.append("")
    lines.append(f"Classification: {report.classification}")
    lines.append(f"Reason: {report.reason}")

    if session.rejected_count > 0:
        lines.append("")
        lines.append("Rejected observations:")
        for obs in session.rejected_observations:
            lines.append(f"  - t={obs.timestamp}: {'; '.join(obs.issues)}")

    return "\n".join(lines)