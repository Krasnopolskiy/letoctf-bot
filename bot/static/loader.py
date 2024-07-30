from pathlib import Path

from aiogram_dialog.widgets.text import Jinja
from jinja2 import Environment

base_path = Path(__file__).parent / "templates"


def load_template_text(name: str) -> str:
    file = base_path / f"{name}.j2"
    with file.open(encoding="utf-8", mode="r") as template:
        return template.read()


def template_widget(name: str) -> Jinja:
    return Jinja(load_template_text(name))


def template_text(name: str, data: dict) -> str:
    env = Environment()
    template = env.from_string(load_template_text(name))
    return template.render(**data)
