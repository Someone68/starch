from config import Config
from kring import get_token
from screens.ftsetup import Setup
from screens.home import Home
from screens.signedout import SignedOut
from screens.signin import SignIn
from textual.app import App
from textual.reactive import Reactive, reactive


class Starch(App):
    SCREENS = {"signed_out": SignedOut, "sign-in": SignIn, "setup": Setup, "home": Home}

    config: reactive[Config] = reactive(Config.load)

    def on_mount(self) -> None:
        server, acc = self.config.active_server, self.config.account
        if server is None:
            self.push_screen("signed_out")
            self.push_screen("setup")
        elif acc and acc.username and get_token(server, acc.username):
            self.push_screen("home")
        else:
            self.push_screen("signed_out")


if __name__ == "__main__":
    Starch().run()
