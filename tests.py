"""Simple scenario checks. Run with: python3 tests.py"""

from models import Participant, Observation, Session
from methods import compute_summaries, classify_session
from data_generator import generate_fitness_data


def build_session(scenario):
    profile, raw_obs = generate_fitness_data(
        participant_id="P001",
        scenario=scenario,
        seed=42,
        number_of_windows=12,
    )
    session = Session(Participant.from_dict(profile))
    for raw in raw_obs:
        session.add_observation(Observation.from_dict(raw))
    return session


def check(scenario, expected):
    session = build_session(scenario)
    summaries = compute_summaries(session)
    label, _ = classify_session(session, summaries)

    ok = (label == expected)
    print(f"{'PASS' if ok else 'FAIL'}  {scenario:<20} expected={expected!r:<22} got={label!r}")
    return ok


def main():
    scenarios = [
        ("resting",           "resting"),
        ("moderate_activity", "moderate activity"),
        ("high_activity",     "high activity"),
        ("recovery",          "recovering"),
        ("poor_quality",      "insufficient data"),
    ]
    results = [check(s, expected) for s, expected in scenarios]
    print(f"\n{sum(results)}/{len(results)} scenarios passed")


if __name__ == "__main__":
    main()