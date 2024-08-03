from datetime import datetime

from pydantic import BaseModel


class TokenRequest(BaseModel):
    username: str
    password: str


class TokenPair(BaseModel):
    access: str
    refresh: str


class Telegram(BaseModel):
    user: str
    tg_id: int
    first_name: str
    last_name: str | None = None
    username: str | None = None


class User(BaseModel):
    id: int
    username: str


class Team(BaseModel):
    id: int
    name: str
    users: list[User]


class JoinTeamRequest(BaseModel):
    user: int
    invite: str


class UserStatistics(BaseModel):
    id: int
    is_staff: bool
    username: str
    team: Team | None
    team_score: float
    team_place: int | None
    personal_score: float
    score: float
    place: int


class S3File(BaseModel):
    id: int
    s3_key: str


class Challenge(BaseModel):
    id: int
    name: str
    description: str | None
    score: int
    team: bool
    review: bool
    hidden: bool
    start: datetime | None
    end: datetime | None
    solved: bool
    files: list[S3File]

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class SubmitChallengeRequest(BaseModel):
    flag: str
    user: int


class UserScore(BaseModel):
    id: int
    username: str
    score: float


class TeamScore(BaseModel):
    id: int
    name: str
    score: float
    users: list[User]


class Event(BaseModel):
    id: int
    title: str
    description: str | None
    speaker: str | None
    affiliation: str | None
    start: datetime
    end: datetime
    files: list[S3File]

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class SubmitFeedbackRequest(BaseModel):
    score: int
    text: str
    user: int
    event: int


class Notification(BaseModel):
    id: int
    title: str
    description: str | None
    type: int
    created_at: datetime
    files: list[S3File]

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class NotificationRecipient(BaseModel):
    id: int
    username: str
