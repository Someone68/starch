from textual.widgets import Footer, Header, Label, Static
from util import StarchScreen


class Home(StarchScreen):
    def compose(self):
        yield Header()
        yield Label(id="signedinas")
        yield Footer()

    def on_screen_resume(self) -> None:
        acc = self.main.config.account
        if acc is None or acc.username is None:
            self.app.switch_screen("signed_out")
            return
        self.query_one("#signedinas", Label).update(f"Signed in as {acc.username}")
