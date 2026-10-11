from config import Config
from screens.ftsetup import Setup
from screens.signedout import SignedOut
from screens.signin import SignIn
from textual.app import App
from textual.reactive import Reactive, reactive


class Starch(App):
    SCREENS = {"signed_out": SignedOut, "sign-in": SignIn, "setup": Setup}

    config: reactive[Config] = reactive(Config.load)

    def on_mount(self) -> None:
        self.push_screen("signed_out")
        if not self.config.server_ip:
            self.push_screen("setup")


if __name__ == "__main__":
    Starch().run()
