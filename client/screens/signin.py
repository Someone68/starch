from reqs import register, signin
from textual.containers import HorizontalGroup, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Input, Label, Static
from util import StarchScreen


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
            signin(
                self.main.server_ip,
                self.query_one("#username", Input).value,
                self.query_one("#password", Input).value,
            )
        else:
            register(
                self.main.server_ip,
                self.query_one("#username", Input).value,
                self.query_one("#password", Input).value,
            )
