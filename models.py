class Participant:
    def __init__(self, participant_id, baseline_heart_rate, baseline_skin_response, baseline_temperature):
        self._participant_id = participant_id
        self.baseline_heart_rate = baseline_heart_rate
        self.baseline_skin_response = baseline_skin_response
        self.baseline_temperature = baseline_temperature

    @property
    def participant_id(self):
        return self._participant_id

    @classmethod
    def from_dict(cls, profile_dict):
        return cls(
            profile_dict["participant_id"],
            profile_dict["baseline_heart_rate"],
            profile_dict["baseline_skin_response"],
            profile_dict["baseline_temperature"],
        )

    def __repr__(self):
        return (f"participant({self._participant_id}, "
                f"hr={self.baseline_heart_rate})")

class Observation:
    HR_MIN, HR_MAX = 35, 205
    TEMP_MIN, TEMP_MAX = 25.0, 42.0
    MIN_SIGNAL_QUALITY = 0.5

    def __init__(self, timestamp, heart_rate, skin_response, temperature, activity_level, signal_quality):
        self.timestamp = timestamp
        self.heart_rate = heart_rate
        self.skin_response = skin_response
        self.temperature = temperature
        self.activity_level = activity_level
        self.signal_quality = signal_quality
        self._issues = self._validate()

    def _validate(self):
        issues = []

        if not isinstance(self.timestamp, int) or self.timestamp < 0:
            issues.append("invalid timestamp")

        if self.heart_rate is None or not (self.HR_MIN <=self.heart_rate <= self.HR_MAX):
            issues.append(f"heart_rate out of range: {self.heart_rate}")

        if self.skin_response is None or self.skin_response < 0:
            issues.append(f"skin_response invalid: {self.skin_response}")

        if self.temperature is None or not (self.TEMP_MIN <= self.temperature <= self.TEMP_MAX):
            issues.append(f"temperature out of range: {self.temperature}")

        if self.activity_level is None or not (0 <= self.activity_level <= 1):
            issues.append(f"activity_level out of range: {self.activity_level}")

        if self.signal_quality is None or not (0 <= self.signal_quality <= 1):
            issues.append(f"signal_quality invalid: {self.signal_quality}")

        elif self.signal_quality < self.MIN_SIGNAL_QUALITY:
            issues.append(f"poor signal quality: {self.signal_quality}")

        return issues

    @property
    def issues(self):
        return list(self._issues)

    @property
    def is_valid(self):
        return len(self._issues) == 0 

    @classmethod
    def from_dict(cls, obs_dict):
        return cls(
            obs_dict.get("timestamp"),
            obs_dict.get("heart_rate"),
            obs_dict.get("skin_response"),
            obs_dict.get("temperature"),
            obs_dict.get("activity_level"),
            obs_dict.get("signal_quality"),
        )

    def __repr__(self):
        return (f"Observation(t={self.timestamp}, "
                f"hr={self.heart_rate}, valid={self.is_valid})")

class Session:

    def __init__(self, participant):
        self.participant = participant
        self.valid_observations = []
        self.rejected_observations = []

    def add_observation(self, observation):
        if observation.is_valid:
            self.valid_observations.append(observation)
        else:
            self.rejected_observations.append(observation)

    @property
    def total_count(self):
        return len(self.valid_observations) + len(self.rejected_observations)

    @property
    def valid_count(self):
        return len(self.valid_observations)

    @property
    def rejected_count(self):
        return len(self.rejected_observations)

    def __repr__(self):
        return (f"session(participant={self.participant.participant_id}, "
                f"valid={self.valid_count}, rejected={self.rejected_count})")

class SessionReport:
    def __init__(self, session, summaries, classification, reason):
        self.session = session
        self.summaries = summaries
        self.classification = classification
        self.reason = reason

    def to_dict(self):
        return {
            "participant_id": self.session.participant.participant_id,
            "total_count": self.summaries["total_count"],
            "valid_count": self.summaries["valid_count"],
            "rejected_count": self.summaries["rejected_count"],
            "average_heart_rate": self.summaries["average_heart_rate"],
            "average_activity": self.summaries["average_activity"],
            "classification": self.classification,
            "reason": self.reason,
        }

    def __repr__(self):
        return (f"SessionReport({self.session.participant.participant_id}, "
                f"{self.classification})")