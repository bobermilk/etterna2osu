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

def clear_note(self) -> None:
    self.query_one(TextLog).clear()

def add_note(self, renderable: RenderableType) -> None:
    self.query_one(TextLog).write(renderable)

def notify(self, message):
    message=message.strip()
    add_note(self.app, message+"\n")
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
        yield Container(
            Horizontal(
            Vertical(
                SectionTitle("Map Attributes"),
                Horizontal(
                    Vertical(
                        Labels("   OD (1 to 10)", classes="label"),
                        Input(placeholder="8"),
                        classes="column"),
                    Vertical(
                        Labels("   HP (1 to 10)", classes="label"),
                        Input(placeholder="7"),
                        classes="column"),
                ),
                Vertical(
                    Labels("   Creator Name", classes="label"),
                    Input(placeholder="Example: bobermilk"),
                ),
                Horizontal(
                    Static("   Remove short lns                            ", classes="btnLabel"),
                    Switch(value=True),
                    classes="container",
                ),
                Horizontal(
                    Static("   Uprate by 0.05 instead of 0.01\n   (warning: this is 2x spam)                  ", classes="btnLabel"),
                    Switch(value=False),
                    classes="container",
                ),
                classes="column",
            ),
            Vertical(
                SectionTitle("Msd restricted rates"),
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
                    Labels("   Maximum msd for rates (1MSD to 100MSD)", classes="label"),
                    Input(placeholder="Example: 28.42"),
                    classes="column"),
                Horizontal(
                    Static("   Show skillset msd in diff names             ", classes="btnLabel"),
                    Switch(value=False),
                    classes="container",
                ),
                Horizontal(
                    Static("   Keep audio pitch in uprates                 ", classes="btnLabel"),
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
        clear_note(self.app)
        log_text=""
        notification_text="Configuration Errors:"
        fail=False
        inputs=[x.value for x in self.query(Input)]

        try:
            OD=int(inputs[0])
        except:
            log_text+="\n"
            log_text+="Warning: Invalid OD, defaulting to OD 8"
            OD=8
        if OD not in range(1,11):
            notification_text+="\n"
            notification_text+="    - OD out of bounds, please retry with a value within 1-10"
            fail=True

        try:
            HP=int(inputs[1])
        except:
            log_text+="\n"
            log_text+="Warning: Invalid HP, defaulting to HP 7"
            HP=7
        if HP not in range(1,11):
            notification_text+="\n"
            notification_text+="    - HP out of bounds, please retry with a value within 1-10"
            fail=True

        try:
            creator=str(inputs[2]).strip()
        except:
            log_text+="\n"
            log_text+="Invalid creator, defaulting to bobermilk"
            creator="bobermilk"
        if not creator:
            log_text+="\n"
            log_text+="Invalid creator, defaulting to bobermilk"
            creator="bobermilk"

        try:
            lowest_rate=float(inputs[3])
        except:
            log_text+="\n"
            log_text+="Warning: Invalid lowest rate, defaulting to 1.0"
            lowest_rate=1.0
        if lowest_rate>1 or lowest_rate<0.8:
            notification_text+="\n"
            notification_text+="    - lowest rate out of bounds, please retry with a value in range 0.8 to 1.0"
            fail=True

        try:
            highest_rate=float(inputs[4])
        except:
            log_text+="\n"
            log_text+="Warning: Invalid highest rate, defaulting to 1.0"
            highest_rate=1.0
        if highest_rate<1.0 or highest_rate>1.45:
            notification_text+="\n"
            notification_text+="    - lowest rate out of bounds, please retry with a value in range 1.0 and 1.45"
            fail=True

        try:
            max_msd=float(inputs[5])
        except:
            log_text+="\n"
            log_text+="Warning: Invalid maximum msd, no msd limit will be set on uprates"
            max_msd=10000.0
        if max_msd<1.0 or max_msd>100.0:
            notification_text+="\n"
            notification_text+="    - lowest rate out of bounds, please retry with a value in range 1.0 and 100.0"
            fail=True

        buttons=[x.value for x in self.query(Switch)]
        remove_ln=buttons[0]
        if remove_ln:
            log_text+="\n"
            log_text+="Warning: Short LNs will be changed to normal note"
        else:
            log_text+="\n"
            log_text+="Warning: Short LNs will remain"

        uprate_half_increments=buttons[1]
        if uprate_half_increments:
            log_text+="\n"
            log_text+="Warning: 0.05 uprate increments will double the number of converted files!"
        show_skillset_msd=buttons[2]
        keep_pitch=buttons[3]
        if not keep_pitch:
            log_text+="\n"
            log_text+="Warning: Disabling keep audio pitch creates nightcore"

        add_note(self.app, log_text +"\n")
        notify(self, notification_text)
        if not fail:
            if show_skillset_msd:
                body.mount(skillset_msd)
            else:
                body.mount(conversion_progress)
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
        ("f1", "app.toggle_class('TextLog', '-hidden')", "Recent Logs"),
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
