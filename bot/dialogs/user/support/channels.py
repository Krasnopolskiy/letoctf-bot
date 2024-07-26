from enum import Enum


class SupportChannel(str, Enum):
    ADMIN = "Административная"
    TECH = "Техническая"
    OTHER = "Прочее"
