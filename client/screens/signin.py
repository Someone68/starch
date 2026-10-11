from nacl.public import PrivateKey
from reqs import register, signin
from textual import work
from textual.containers import HorizontalGroup, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Input, Label, Static
from textual.worker import Worker, WorkerState
from util import StarchScreen

from client.kring import set_token


class SignIn(StarchScreen):
    def on_mount(self) -> None:
        self.watch(self.main, "server_ip", self._show_server)

    def compose(self):
        yield Header()
        with Vertical(classes="card"):
            yield Label("Connected to server: none", classes="title", id="server")
            yield Input(placeholder="username", id="username")
            yield Input(placeholder="password", id="password", password=True)
            with HorizontalGroup(classes="buttons"):
                yield Button("Sign in", id="sign-in", variant="primary")
                yield Button("Register", id="register", variant="primary")
        yield Footer()

    def _show_server(self, ip: str | None) -> None:
        self.query_one("#server", Label).update(f"Connected to server: {ip or 'none'}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "sign-in":
            self._signin(
                self.main.config.server_ip,
                self.query_one("#username", Input).value,
                self.query_one("#password", Input).value,
            )
        else:
            self._register(
                self.main.config.server_ip,
                self.query_one("#username", Input).value,
                self.query_one("#password", Input).value,
            )

    @work(thread=True, exclusive=True)
    def _signin(self, ip: str, username: str, password: str) -> str:
        return signin(ip, username, password)

    @work(thread=True, exclusive=True)
    def _register(
        self, ip: str, username: str, password: str
    ) -> tuple[int, PrivateKey]:
        return register(ip, username, password)

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        if event.state == WorkerState.SUCCESS:
            if event.worker.name == "_signin" and type(event.worker.result) == str:
                # todo: rework how tokens and keys are stored
                set_token(self.main.config.server_ip or "unknown", event.worker.result)
                self.notify("Login sucessful!", severity="information")
            elif event.worker.name == "_register":
                # todo: save private key and stuff
                self.notify("Registration sucessful!", severity="information")
