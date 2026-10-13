from textual.widgets import Footer, Header, Static
from util import StarchScreen


class Home(StarchScreen):
    def compose(self):
        yield Header()
        yield Static("Home screen")
        yield Footer()
