# Smart Fitness Session Analyzer

**Option A** — Smart Fitness Session Analyzer

- **Student name:** Roshan Khadka
- **Student number:** 416278
  **Student email:** rokha9526@oslomet.no
- **Repository:** https://github.com/Jan9e/Smart-Fitness-Session-Analyzer

## Description

A Python program that reads simulated wearable-device measurements from
training sessions. It validates each measurement, groups observations
into a session, calculates summaries, compares them to a participant's
personal baseline, classifies the session, detects recovery, and prints
a readable report.

## Project structure

- `main.py` — entry point; runs all five scenarios and prints a report for each.
- `models.py` — domain classes: `Participant`, `Observation`, `Session`, `SessionReport`.
- `methods.py` — standalone functions for summaries, classification, recovery, and reporting.
- `tests.py` — automated scenario checks.
- `data_generator.py` — instructor-supplied simulated data generator.
- `requirements.txt` — states that only the Python standard library is used.

## Class design

| Class | Responsibility |
|---|---|
| `Participant` | Stores participant ID and personal reference values (heart rate, skin response, temperature). |
| `Observation` | Represents one sensor window and validates its own values. |
| `Session` | Groups one participant with lists of valid and rejected observations. |
| `SessionReport` | Holds the session, its summaries, and its classification; can be converted to a dictionary. |

## OOP concepts demonstrated

- **Composition:** `Session` HAS-A `Participant` and HAS-MANY `Observation` objects.
- **Encapsulation:** `Participant._participant_id` and `Observation._issues` are protected and exposed through properties.
- **Class methods:** `Participant.from_dict()` and `Observation.from_dict()` act as factory methods that build objects from the raw generator dictionaries.

## Why composition instead of inheritance

This project deliberately uses composition instead of inheritance.

A `Session` is not a *kind of* `Participant`, nor a *kind of*
`Observation`. A session genuinely *has* a participant and *has many*
observations. Modelling that as inheritance would force an artificial
"is-a" relationship that does not match the domain.

Composition lets us:

1. Keep `Observation` self-validating and reusable.
2. Swap participants between sessions freely.
3. Build a `SessionReport` from any session without subclassing.

This is the assignment's permitted alternative to inheritance: a justified written explanation of why composition is the correct design.

## Assumptions and classification rules

**Validation rules:**

- `heart_rate`: must be between 35 and 205 bpm.
- `temperature`: must be between 25 and 42 °C.
- `activity_level`: must be between 0 and 1.
- `skin_response`: must be non-negative.
- `signal_quality`: below 0.5 is treated as unusable.
- Missing (`None`) or impossible values cause the observation to be rejected.

**Classification rules (checked in this order):**

- `insufficient data` — fewer than 3 valid observations.
- `recovering` — first third of the session had average heart rate more than 20 bpm above baseline, and the last third dropped by at least 15 bpm with activity down by at least 0.2.
- `resting` — average activity below 0.25 and average heart rate within 10 bpm of baseline.
- `high activity` — average activity above 0.65 or average heart rate more than 40 bpm above baseline.
- `moderate activity` — anything else.

## Installation and running

No external packages are required. Only the Python standard library.

```bash
git clone https://github.com/Jan9e/Smart-Fitness-Session-Analyzer.git
cd Smart-Fitness-Session-Analyzer
python3 main.py      # runs all five scenarios
python3 tests.py     # runs the automated scenario checks
```

************ Output for python3 main.py ******************

########## Scenario: resting ##########
=== Session report for participant P001 ===
Baseline heart rate: 78 bpm
Baseline skin response: 1.17
Baseline temperature: 32.76 °C

Total observations: 12
Valid observations: 12
Rejected observations: 0

Average heart rate: 80.0 bpm (min 76, max 85)
Average activity level: 0.11 (min 0.04, max 0.18)
Average skin response: 1.19
Average temperature: 32.78 °C
Average signal quality: 0.91

Classification: resting
Reason: low activity (0.11) and heart rate near baseline (80 vs 78 bpm)


########## Scenario: moderate_activity ##########
=== Session report for participant P001 ===
Baseline heart rate: 78 bpm
Baseline skin response: 1.17
Baseline temperature: 32.76 °C

Total observations: 12
Valid observations: 12
Rejected observations: 0

Average heart rate: 105.8 bpm (min 97, max 116)
Average activity level: 0.51 (min 0.39, max 0.62)
Average skin response: 1.51
Average temperature: 33.03 °C
Average signal quality: 0.91

Classification: moderate activity
Reason: moderate activity (0.51) and heart rate above baseline (106 vs 78 bpm)


########## Scenario: high_activity ##########
=== Session report for participant P001 ===
Baseline heart rate: 78 bpm
Baseline skin response: 1.17
Baseline temperature: 32.76 °C

Total observations: 12
Valid observations: 12
Rejected observations: 0

Average heart rate: 135.7 bpm (min 123, max 150)
Average activity level: 0.80 (min 0.69, max 0.91)
Average skin response: 1.80
Average temperature: 33.34 °C
Average signal quality: 0.91

Classification: high activity
Reason: high activity (0.80) or heart rate well above baseline (136 vs 78 bpm)


########## Scenario: recovery ##########
=== Session report for participant P001 ===
Baseline heart rate: 78 bpm
Baseline skin response: 1.17
Baseline temperature: 32.76 °C

Total observations: 12
Valid observations: 12
Rejected observations: 0

Average heart rate: 112.8 bpm (min 86, max 141)
Average activity level: 0.48 (min 0.10, max 0.88)
Average skin response: 1.57
Average temperature: 33.05 °C
Average signal quality: 0.91

Classification: recovering
Reason: heart rate and activity declined near the end of the session


########## Scenario: poor_quality ##########
=== Session report for participant P001 ===
Baseline heart rate: 78 bpm
Baseline skin response: 1.17
Baseline temperature: 32.76 °C

Total observations: 12
Valid observations: 0
Rejected observations: 12

No valid observations to summarise.

Classification: insufficient data
Reason: fewer than 3 valid observations

Rejected observations:
  - t=0: heart_rate out of range: None; poor signal quality: 0.07
  - t=1: heart_rate out of range: 265; poor signal quality: 0.41
  - t=2: activity_level out of range: -0.2; poor signal quality: 0.13
  - t=3: skin_response invalid: None; poor signal quality: 0.1
  - t=4: heart_rate out of range: None; poor signal quality: 0.11
  - t=5: heart_rate out of range: 265; poor signal quality: 0.49
  - t=6: activity_level out of range: -0.2; poor signal quality: 0.48
  - t=7: skin_response invalid: None; poor signal quality: 0.13
  - t=8: heart_rate out of range: None; poor signal quality: 0.32
  - t=9: heart_rate out of range: 265; poor signal quality: 0.39
  - t=10: activity_level out of range: -0.2; poor signal quality: 0.25
  - t=11: skin_response invalid: None; poor signal quality: 0.16


  ************************Output for python3 test,py*********************************

PASS  resting              expected='resting'              got='resting'
PASS  moderate_activity    expected='moderate activity'    got='moderate activity'
PASS  high_activity        expected='high activity'        got='high activity'
PASS  recovery             expected='recovering'           got='recovering'
PASS  poor_quality         expected='insufficient data'    got='insufficient data'

5/5 scenarios passed