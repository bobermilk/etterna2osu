# to use in command line: textual console

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.containers import Container, Horizontal, Vertical

from rich.console import RenderableType
from rich.markdown import Markdown
from rich.text import Text

from textual.widgets import (
    Button,
    Footer,
    Header,
    Input,
    Static,
    Switch,
    TextLog,
)

def add_note(self, renderable: RenderableType) -> None:
    self.query_one(TextLog).write(renderable)

def notify(self, message):
    self.app.bell()
    message=Text.assemble(message)
    self.screen.mount(Notification(message))

class Notification(Static):
    def on_mount(self) -> None:
        self.set_timer(3, self.remove)

    def on_click(self) -> None:
        self.remove()

class Labels(Static):
    pass

class SectionTitle(Labels):
    pass

class Body(Container):
    def compose(self) -> ComposeResult:
        yield Container(
            TextLog(classes="-hidden", wrap=False, highlight=True, markup=True),
            configuration,
        )

class Welcome(Container):
    def compose(self) -> ComposeResult:
        yield Labels(Markdown("# hello"))
        yield Button("Start", variant="success")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        body.mount(ChartAttributes())
        welcome.remove()

class ChartAttributes(Container):
    def compose(self) -> ComposeResult:
        notify(self, "pizza\nhut\nis\ncool")
        yield Container(
            Horizontal(
            Vertical(
                SectionTitle("Map Attributes"),
                Horizontal(
                    Vertical(
                        Labels("   OD", classes="label"),
                        Input(placeholder="8"),
                        classes="column"),
                    Vertical(
                        Labels("   HP", classes="label"),
                        Input(placeholder="7"),
                        classes="column"),
                ),
                Vertical(
                    Labels("   Creator Name", classes="label"),
                    Input(value="bobermilk", placeholder="bobermilk"),
                ),
                Horizontal(
                    Static("   Remove short lns:                           ", classes="btnLabel"),
                    Switch(value=True),
                    classes="container",
                ),
                Horizontal(
                    Static("   Uprate by 0.05 instead of 0.01\n   (warning: this is 2x spam):                 ", classes="btnLabel"),
                    Switch(value=False),
                    classes="container",
                ),
                classes="column",
            ),
            Vertical(
                SectionTitle("Map Attributes"),
                Horizontal(
                    Vertical(
                        Labels("   Lowest rate (0.8 min)", classes="label"),
                        Input(placeholder="Example: 0.8"),
                        classes="column"),
                    Vertical(
                        Labels("   Highest rate (1.45 max)", classes="label"),
                        Input(placeholder="Example: 1.35"),
                        classes="column"),
                ),
                Vertical(
                    Labels("   Maximum msd to restrict further uprates", classes="label"),
                    Input(placeholder="Example: 28.42"),
                    classes="column"),
                Horizontal(
                    Static("   Show skillset msd in diff names:            ", classes="btnLabel"),
                    Switch(value=False),
                    classes="container",
                ),
                Horizontal(
                    Static("   Keep audio pitch in uprates:                ", classes="btnLabel"),
                    Switch(value=True),
                    classes="container",
                ),
                classes="column",
            ),
        ),
        Button("Start Conversion", variant="primary"),
        Static(),
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        inputs=self.query(Input)
        try:
            OD=int(inputs[0])
        except:
            notify(self, "Invalid HP, defaulting to HP 7")
        HP=inputs[1]
        creator=inputs[2]
        lowest_rate=inputs[3]
        higest_rate=inputs[4]
        min_msd=inputs[5]

        buttons=self.query(Switch)
        remove_ln=buttons[0]
        uprate_half_increments=buttons[1]
        show_skillset_msd=buttons[2]
        keep_pitch=buttons[3]

        self.remove()


class SkillsetMsd(Container):
    def compose(self) -> ComposeResult:
        yield Labels()

class ConversionProgress(Container):
    def compose(self) -> ComposeResult:
        yield Labels()

# LinearLayout (https://textual.textualize.io/guide/layout/)
body=Body()
welcome=Welcome()
configuration=ChartAttributes()
skillset_msd=SkillsetMsd()
conversion_progress=ConversionProgress()

class etterna2osu(App):
    CSS_PATH = "gui.css"
    BINDINGS = [("ctrl+d", "toggle_dark", "Toggle dark mode"),
        ("ctrl+c", "app.quit", "Quit"),
        ("f1", "app.toggle_class('TextLog', '-hidden')", "Notes"),
        ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield body

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

if __name__ == "__main__":
    app = etterna2osu()
    app.run()
