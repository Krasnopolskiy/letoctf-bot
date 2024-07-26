from pathlib import Path

from aiogram_dialog.widgets.text import Jinja

base_path = Path(__file__).parent / "templates"


def load_template(name: str) -> Jinja:
    file = base_path / f"{name}.j2"
    with file.open(encoding="utf-8", mode="r") as template:
        return Jinja(template.read())
