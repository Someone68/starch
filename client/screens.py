import json
from pydoc import getpager

from requests import get, post
from requests.exceptions import RequestException
from textual import work
from textual.containers import Center, CenterMiddle, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Input, Label, Static
from textual.worker import Worker, WorkerState
from util import normalize_url


class SignedOut(Screen):
    def compose(self):
        yield Header()
        with Vertical(classes="card"):
            yield Label("Connected to server:", classes="title")
            yield Static("You are not signed in.", classes="title")
            yield Button("Sign in / Register", id="sign-in", variant="primary")
        yield Footer()


class Setup(Screen):
    def compose(self):
        yield Header()
        with Center(classes="card"):
            yield Static("First-time setup", classes="title")
            yield Static("Starch requires you to connect to a server to function.")
            yield Input(
                placeholder="Server IP",
                id="server-url",
            )
            yield Button("Connect", id="connect", variant="primary")

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id != "connect":
            return
        field = self.query_one("#server-url", Input)
        try:
            url = normalize_url(field.value)
        except ValueError as e:
            self.notify(str(e), severity="error")
            return
        self.notify("Connecting...")
        self.connect(url)

    @work(thread=True, exclusive=True, exit_on_error=False, name="connect")
    def connect(self, url: str) -> bool:
        return try_connect(url)

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        if event.worker.name != "connect":
            return

        running = event.state in (WorkerState.PENDING, WorkerState.RUNNING)
        url_input = self.query_one("#server-url", Input)
        url_input.disabled = running
        self.query_one("#connect", Button).disabled = running
        if running:
            return

        failed = event.state == WorkerState.ERROR or (
            event.state == WorkerState.SUCCESS and not event.worker.result
        )
        if failed:
            self.notify("Connection failed", severity="error")
            self.call_after_refresh(url_input.focus)
            return

        self.notify("Connected")
        self.app.pop_screen()


def try_connect(server_url: str) -> bool:
    try:
        r = get(f"{server_url}/check-starch", timeout=5)
    except RequestException:
        return False

    if r.status_code != 200:
        return False
    if not r.headers.get("Content-Type", "").startswith("application/json"):
        return False
    try:
        data = r.json()
    except ValueError:
        return False

    return isinstance(data, dict) and data.get("app") == "starch"
