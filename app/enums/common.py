from enum import Enum


class EnvironmentEnum(str, Enum):
    LOCAL = "LOCAL"
    DEVELOPMENT = "DEVELOPMENT"
    STAGE = "STAGE"
    PRODUCTION = "PRODUCTION"
