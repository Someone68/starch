from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, Static
from util import StarchScreen


class SignedOut(StarchScreen):
    def compose(self):
        yield Header()
        with Vertical(classes="card"):
            yield Label(
                f"Connected to server: {self.main.config.active_server or 'none'}",
                classes="title",
                id="server",
            )
            yield Static("You are not signed in.", classes="title")
            yield Button("Sign in / Register", id="sign-in", variant="primary")
        yield Footer()

    def on_screen_resume(self) -> None:
        server = self.main.config.active_server
        self.query_one("#server", Label).update(
            f"Connected to server: {server or 'none'}"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "sign-in":
            self.app.switch_screen("sign-in")
