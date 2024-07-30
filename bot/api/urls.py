from enum import Enum

from config.bot import bot


class BaseEndpoint(str, Enum):
    pass


class AuthEndpoint(BaseEndpoint):
    TOKEN = "/api/auth/token/"
    TELEGRAM_LINK = "/api/auth/telegram/staff/"
    TELEGRAM_GET = "/api/auth/telegram/{tg_id}/"


class TeamEndpoint(BaseEndpoint):
    JOIN = "/api/teams/join/"


class StatisticsEndpoint(BaseEndpoint):
    STATISTICS = "/api/statistics/{id}/"


class ChallengeEndpoint(BaseEndpoint):
    LIST = "/api/challenges/"
    DETAIL = "/api/challenges/{id}/"
    SUBMIT = "/api/challenges/{id}/submit/staff/"
    SUBMIT_HIDDEN = "/api/challenges/submit/staff/"


class ScoreboardEndpoint(BaseEndpoint):
    USERS = "/api/scoreboard/users/"
    TEAMS = "/api/scoreboard/teams/"


class EventEndpoint(BaseEndpoint):
    LIST = "/api/events/"
    DETAIL = "/api/events/{id}/"


class NotificationEndpoint(BaseEndpoint):
    LIST = "/api/notifications/"
    DETAIL = "/api/notifications/{id}/"
    LIST_STAFF = "/api/staff/notifications/"
    DETAIL_STAFF = "/api/staff/notifications/{id}/"
    RECIPIENTS = "/api/staff/notifications/{id}/recipients/"


def reverse(endpoint: BaseEndpoint, **kwargs) -> str:
    try:
        return bot.api_url + endpoint.value.format(**kwargs)
    except KeyError as exc:
        raise KeyError("Invalid reverse params") from exc
