import sys
from Qt import QtWidgets, QtGui
from .lib import (
    BTN_FIXED_SIZE,
    CHILD_OFFSET
)
from .local_settings import LocalSettingsWindow
from .settings import (
    style,
    MainWidget,
    ProjectListWidget
)


def main(user_role=None):
    if user_role is None:
        user_role = "manager"

    user_role_low = user_role.lower()
    allowed_roles = ("developer", "manager")
    if user_role_low not in allowed_roles:
        raise ValueError("Invalid user role \"{}\". Expected {}".format(
            user_role, ", ".join(allowed_roles)
        ))

    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(style.app_icon_path()))

    widget = MainWidget(user_role)
    widget.show()

    sys.exit(app.exec_())


__all__ = (
    "BTN_FIXED_SIZE",
    "CHILD_OFFSET",

    "style",

    "MainWidget",
    "ProjectListWidget",
    "LocalSettingsWindow",
    "main"
)
