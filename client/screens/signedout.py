from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, Static
from util import StarchScreen


class SignedOut(StarchScreen):
    def on_mount(self) -> None:
        self.watch(self.main, "server_ip", self._show_server)

    def compose(self):
        yield Header()
        with Vertical(classes="card"):
            yield Label("Connected to server: none", classes="title", id="server")
            yield Static("You are not signed in.", classes="title")
            yield Button("Sign in / Register", id="sign-in", variant="primary")
        yield Footer()

    def _show_server(self, ip: str | None) -> None:
        self.query_one("#server", Label).update(f"Connected to server: {ip or 'none'}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "sign-in":
            self.app.switch_screen("sign-in")
