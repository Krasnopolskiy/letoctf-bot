from dialogs.user.challenges.dialog import challenges_dialog
from dialogs.user.events.dialog import events_dialog
from dialogs.user.menu.dialog import menu_dialog
from dialogs.user.notifications.dialog import notifications_dialog
from dialogs.user.scoreboard.dialog import scoreboard_dialog
from dialogs.user.support.dialog import support_dialog
from dialogs.user.teams.dialog import teams_dialog


def user_dialogs():
    menu_dialog()
    challenges_dialog()
    events_dialog()
    scoreboard_dialog()
    teams_dialog()
    notifications_dialog()
    support_dialog()
