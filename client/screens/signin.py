from kring import set_private_key, set_token
from reqs import register, signin
from textual import work
from textual.containers import HorizontalGroup, Vertical
from textual.widgets import Button, Footer, Header, Input, Label
from textual.worker import Worker, WorkerState
from util import AUTH_ERRORS, AuthResult, StarchScreen


class SignIn(StarchScreen):
    def compose(self):
        yield Header()
        with Vertical(classes="card"):
            yield Label(
                f"Connected to server: {self.main.config.active_server or 'none'}",
                classes="title",
                id="server",
            )
            yield Input(placeholder="username", id="username")
            yield Input(placeholder="password", id="password", password=True)
            with HorizontalGroup(classes="buttons"):
                yield Button("Sign in", id="sign-in", variant="primary")
                yield Button("Register", id="register", variant="primary")
        yield Footer()

    def on_screen_resume(self) -> None:
        server = self.main.config.active_server
        self.query_one("#server", Label).update(
            f"Connected to server: {server or 'none'}"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        server = self.main.config.active_server
        username = self.query_one("#username", Input).value
        password = self.query_one("#password", Input).value
        if len(password) < 8:
            self.notify("Password must be at least 8 characters long", severity="error")
            return
        if len(username) < 3:
            self.notify("Username must be at least 3 characters long", severity="error")
            return
        if len(username) > 32:
            self.notify("Username must be at most 32 characters long", severity="error")
            return
        if not server:
            self.notify("No server connected", severity="error")
            return
        if not username or not password:
            self.notify("Fill out all fields to continue", severity="error")
            return
        if event.button.id == "sign-in":
            self._signin(server, username, password)
        else:
            self._register(server, username, password)

    @work(thread=True, exclusive=True)
    def _signin(self, ip: str, username: str, password: str) -> AuthResult:
        status, token = signin(ip, username, password)
        return AuthResult("signin", status, ip, username, token)

    @work(thread=True, exclusive=True)
    def _register(self, ip: str, username: str, password: str) -> AuthResult:
        status, private_key = register(ip, username, password)
        if status != 201 or not private_key:
            return AuthResult("register", status, ip, username)

        set_private_key(ip, username, private_key)

        status, token = signin(ip, username, password)
        return AuthResult("signin", status, ip, username, token or None)

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        if event.worker.name not in ("_signin", "_register"):
            return
        if event.state == WorkerState.ERROR:
            self.notify(f"Error: {event.worker.error}", severity="error")
            return
        if event.state != WorkerState.SUCCESS:
            return

        result = event.worker.result
        assert isinstance(result, AuthResult)

        if result.status != 200 or not result.token:
            msg = AUTH_ERRORS.get(
                (result.step, result.status),
                f"{result.step.title()} failed ({result.status})",
            )
            self.notify(msg, severity="error")
            return

        set_token(result.server, result.username, result.token)
        acc = self.main.config.servers[result.server]
        acc.username = result.username
        self.main.config.save()
        self.notify(f"{result.step.title()} successful", severity="information")
        self.main.switch_screen("home")
