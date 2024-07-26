from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Row, Start
from aiogram_dialog.widgets.text import Const
from dialogs.user.challenges.states import UserChallengesStateGroup
from dialogs.user.events.states import UserEventsStateGroup
from dialogs.user.menu.states import UserMenuStateGroup
from dialogs.user.notifications.states import UserNotificationsStateGroup
from dialogs.user.scoreboard.states import UserScoreboardStateGroup
from dialogs.user.support.states import UserSupportStateGroup
from dialogs.user.teams.states import UserTeamsStateGroup
from handlers.user.menu import get_user_statistics, not_in_team
from static.loader import load_template

menu = Window(
    load_template("statistics"),
    Start(Const("🤝 Присоединиться к команде"), id="teams", state=UserTeamsStateGroup.join, when=not_in_team),
    Row(
        Start(Const("🏅 Личный рейтинг"), id="personal_rating", state=UserScoreboardStateGroup.users),
        Start(Const("🏆 Командный рейтинг"), id="team_rating", state=UserScoreboardStateGroup.teams),
    ),
    Row(
        Start(Const("🎯 Задачи"), id="challenges", state=UserChallengesStateGroup.list),
        Start(Const("📆 Мероприятия"), id="events", state=UserEventsStateGroup.list),
        Start(Const("📫 Сообщения"), id="notifications", state=UserNotificationsStateGroup.list),
    ),
    Start(Const("🆘 Поддержка"), id="support", state=UserSupportStateGroup.support),
    state=UserMenuStateGroup.menu,
    getter=get_user_statistics,
)
