from enum import Enum, auto


class IdType(Enum):
    CEDULA = auto()
    PASAPORTE = auto()
    NIT = auto()
    EXTRANJERIA = auto()