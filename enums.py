from enum import Enum


class Colors(str, Enum):
    GREEN = 'green'
    RED = 'red'
    BLUE = 'blue'
    YELLOW = 'yellow'


class Formats(str, Enum):
    DEFAULT = "default"
    TABLE = "table"
    JSON = "json"


class Periods(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class ContentTypes(str, Enum):
    REPOSITORIES = "repositories"
    DEVELOPERS = "developers"
