from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel

from dialogs.user.scoreboard.states import UserScoreboardStateGroup
from dialogs.widgets import back
from handlers.user.scoreboard import render_teams, render_users
from static.loader import template_widget

users = Window(
    template_widget("scoreboard/users"),
    Cancel(back, id="back"),
    state=UserScoreboardStateGroup.users,
    getter=render_users,
)

teams = Window(
    template_widget("scoreboard/teams"),
    Cancel(back, id="back"),
    state=UserScoreboardStateGroup.teams,
    getter=render_teams,
)
