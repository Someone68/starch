from screens import Setup, SignedOut
from textual.app import App, ComposeResult
from textual.widgets import Button, Footer, Header, Static


class Starch(App):
    SCREENS = {"signed_out": SignedOut, "setup": Setup}

    def on_mount(self) -> None:
        self.push_screen("signed_out")
        self.push_screen("setup")


if __name__ == "__main__":
    Starch().run()
