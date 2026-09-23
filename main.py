"""Runs every scenario and prints a report for each."""

from data_generator import available_scenarios, generate_fitness_data
from models import Participant, Observation, Session, SessionReport
from methods import compute_summaries, classify_session, format_report


def run_scenario(scenario):
    profile, raw_obs = generate_fitness_data(
        participant_id="P001",
        scenario=scenario,
        seed=42,
        number_of_windows=12,
    )

    participant = Participant.from_dict(profile)
    session = Session(participant)
    for raw in raw_obs:
        session.add_observation(Observation.from_dict(raw))

    summaries = compute_summaries(session)
    classification, reason = classify_session(session, summaries)
    report = SessionReport(session, summaries, classification, reason)

    print(f"\n########## Scenario: {scenario} ##########")
    print(format_report(report))


def main():
    for scenario in available_scenarios():
        run_scenario(scenario)


if __name__ == "__main__":
    main()