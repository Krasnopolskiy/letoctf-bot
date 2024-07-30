import jwt
from aiohttp import ClientSession

from api.structs import (
    Challenge,
    Event,
    JoinTeamRequest,
    Notification,
    NotificationRecipient,
    SubmitChallengeRequest,
    TeamScore,
    Telegram,
    TokenPair,
    TokenRequest,
    User,
    UserScore,
    UserStatistics,
)
from api.urls import (
    AuthEndpoint,
    ChallengeEndpoint,
    EventEndpoint,
    NotificationEndpoint,
    ScoreboardEndpoint,
    StatisticsEndpoint,
    TeamEndpoint,
    reverse,
)
from config.bot import bot
from config.redis import redis


class APIClient:
    def __init__(self):
        self.session = None
        self.cache = redis.redis

    async def __aenter__(self):
        self.session = ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def get_authorization_header(self):
        access_token = await self.cache.get("access_token")
        if not access_token:
            access_token = await self.get_token(bot.api_username, bot.api_password)
        return {"Authorization": f"Bearer {access_token}"}

    async def setup_tokens(self, access_token: str, refresh_token: str):
        access_lifetime = jwt.decode(access_token, options={"verify_signature": False})["exp"]
        await self.cache.set("access_token", access_token, exat=access_lifetime)

        refresh_lifetime = jwt.decode(refresh_token, options={"verify_signature": False})["exp"]
        await self.cache.set("refresh_token", refresh_token, exat=refresh_lifetime)

    async def get_token(self, username: str, password: str) -> str:
        url = reverse(AuthEndpoint.TOKEN)
        data = TokenRequest(username=username, password=password).model_dump()
        async with self.session.post(url, json=data) as response:
            response.raise_for_status()
            token_response = TokenPair(**await response.json())
            await self.setup_tokens(token_response.access, token_response.refresh)
            return token_response.access

    async def link_telegram(self, request: Telegram):
        url = reverse(AuthEndpoint.TELEGRAM_LINK)
        headers = await self.get_authorization_header()
        async with self.session.post(url, json=request.model_dump(), headers=headers):
            pass

    async def get_user_by_tg_id(self, tg_id: int) -> User | None:
        url = reverse(AuthEndpoint.TELEGRAM_GET, tg_id=tg_id)
        async with self.session.get(url) as response:
            if response.status != 200:
                return None
            return User(**await response.json())

    async def join_team(self, request: JoinTeamRequest) -> bool:
        url = reverse(TeamEndpoint.JOIN)
        async with self.session.post(url, data=request.model_dump()) as response:
            return response.status == 200

    async def get_user_statistics(self, user_id: int) -> UserStatistics:
        url = reverse(StatisticsEndpoint.STATISTICS, id=user_id)
        async with self.session.get(url) as response:
            response.raise_for_status()
            return UserStatistics(**await response.json())

    async def get_challenges(self, user_id: int | None = None) -> list[Challenge]:
        url = reverse(ChallengeEndpoint.LIST) + (f"?user_id={user_id}" if user_id else "")
        headers = await self.get_authorization_header()
        async with self.session.get(url, headers=headers) as response:
            response.raise_for_status()
            challenges_data = await response.json()
            return [Challenge(**challenge) for challenge in challenges_data]

    async def get_challenge(self, challenge_id: int, user_id: int | None = None) -> Challenge:
        url = reverse(ChallengeEndpoint.DETAIL, id=challenge_id) + (f"?user_id={user_id}" if user_id else "")
        headers = await self.get_authorization_header()
        async with self.session.get(url, headers=headers) as response:
            response.raise_for_status()
            return Challenge(**await response.json())

    async def submit_challenge(self, challenge_id: int, request: SubmitChallengeRequest) -> bool:
        url = reverse(ChallengeEndpoint.SUBMIT, id=challenge_id)
        headers = await self.get_authorization_header()
        async with self.session.post(url, json=request.model_dump(), headers=headers) as response:
            if response.status == 404:
                return False
            result = await response.json()
            return result["correct"]

    async def submit_hidden_challenge(self, request: SubmitChallengeRequest) -> bool:
        url = reverse(ChallengeEndpoint.SUBMIT_HIDDEN)
        headers = await self.get_authorization_header()
        async with self.session.post(url, json=request.model_dump(), headers=headers) as response:
            if response.status == 404:
                return False
            result = await response.json()
            return result["correct"]

    async def get_users_scoreboard(self) -> list[UserScore]:
        url = reverse(ScoreboardEndpoint.USERS)
        headers = await self.get_authorization_header()
        async with self.session.get(url, headers=headers) as response:
            response.raise_for_status()
            scoreboard_data = await response.json()
            return [UserScore(**score) for score in scoreboard_data]

    async def get_teams_scoreboard(self) -> list[TeamScore]:
        url = reverse(ScoreboardEndpoint.TEAMS)
        headers = await self.get_authorization_header()
        async with self.session.get(url, headers=headers) as response:
            response.raise_for_status()
            scoreboard_data = await response.json()
            return [TeamScore(**score) for score in scoreboard_data]

    async def get_events(self) -> list[Event]:
        url = reverse(EventEndpoint.LIST)
        async with self.session.get(url) as response:
            response.raise_for_status()
            events_data = await response.json()
            return [Event(**event) for event in events_data]

    async def get_event(self, event_id: int) -> Event:
        url = reverse(EventEndpoint.DETAIL, id=event_id)
        async with self.session.get(url) as response:
            response.raise_for_status()
            return Event(**await response.json())

    async def get_notifications(self, user_id: int | None = None) -> list[Notification]:
        url = reverse(NotificationEndpoint.LIST) + (f"?user_id={user_id}" if user_id else "")
        async with self.session.get(url) as response:
            response.raise_for_status()
            notifications_data = await response.json()
            return [Notification(**notification) for notification in notifications_data]

    async def get_notification(self, notification_id: int, user_id: int | None = None) -> Notification:
        url = reverse(NotificationEndpoint.DETAIL, id=notification_id) + (f"?user_id={user_id}" if user_id else "")
        async with self.session.get(url) as response:
            response.raise_for_status()
            return Notification(**await response.json())

    async def get_notifications_staff(self) -> list[Notification]:
        url = reverse(NotificationEndpoint.LIST_STAFF)
        headers = await self.get_authorization_header()
        async with self.session.get(url, headers=headers) as response:
            response.raise_for_status()
            notifications_data = await response.json()
            return [Notification(**notification) for notification in notifications_data]

    async def get_notification_staff(self, notification_id: int) -> Notification:
        url = reverse(NotificationEndpoint.DETAIL_STAFF, id=notification_id)
        headers = await self.get_authorization_header()
        async with self.session.get(url, headers=headers) as response:
            response.raise_for_status()
            return Notification(**await response.json())

    async def get_notification_recipients(self, notification_id: int) -> list[NotificationRecipient]:
        url = reverse(NotificationEndpoint.RECIPIENTS, id=notification_id)
        headers = await self.get_authorization_header()
        async with self.session.get(url, headers=headers) as response:
            response.raise_for_status()
            recipients_data = await response.json()
            return [NotificationRecipient(**recipient) for recipient in recipients_data]
