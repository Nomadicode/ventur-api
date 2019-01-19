from enum import Enum


class RepeatOptions(Enum):
    NONE = "No Repeat"
    DAY = "Daily"
    WEEK = "Weekly"
    MONTH = "Monthly"
    WEEKDAY = "Weekday"
    WEEKEND = "Weekend"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class ReportOptions(Enum):
    SPAM = "This activity is spam"
    ABUSIVE = "This activity is abusive or harassing"
    HATE = "This activity includes hate speach"
    MINORS = "This activity "
    PORN = "This activity contains pornographic content"
    ILLEGAL = "This activity contains illegal content"
    RISKY = "This activity encourages risky behavior"
    OTHER = "Something not listed"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
