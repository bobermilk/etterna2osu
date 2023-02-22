# to use in command line: textual console

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.containers import Container, Horizontal, Vertical

from rich.console import RenderableType
from rich.markdown import Markdown
from rich.text import Text

import util

from textual.widgets import (
    Button,
    Footer,
    Header,
    Input,
    Static,
    Switch,
)

# def clear_note(self) -> None:
#     self.query_one(TextLog).clear()

# def add_note(self, renderable: RenderableType) -> None:
#     self.query_one(TextLog).write(renderable)

def notify(self, message):
    message=message.strip()
    # add_note(self.app, message+"\n")
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
        yield welcome

class Welcome(Container):
    def compose(self) -> ComposeResult:
        yield Labels(Markdown(f"# etterna2osu v{util.APP_VERSION} by bobermilk\n"+
                              "## Thank you demi, kangalio, nakadashi, guil, marc, chxu, senya, gonx, messica for helping\n"+
                              "### DM milk#6867 on discord for any queries after reading FAQs at https://milkies.ml/etterna2osu\n"+
                              "### bobermilk is not liable for any distribution of the converted packs, only upload your own charts"), classes="chicken")
        yield Button("Start", variant="success")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        body.mount(ChartAttributes())
        welcome.remove()

OD=8
HP=7
offset=-26
creator="bobermilk"
additional_tags=""
rates=[0,0,0] # initial, step size, number
msd_bounds=[0,0] #min_msd, max_msd
remove_ln=False
diff_name_skillset_msd=[False]*7 # Str, JS, HS, Stamina, JaSp, CJ, Tech
keep_pitch=True

class ChartAttributes(Container):
    def compose(self) -> ComposeResult:
        yield Container(
            Horizontal(
            Vertical(
                SectionTitle("Map Attributes"),
                Static(),
                Horizontal(
                    Vertical(
                        Labels(" OD (1 to 10)", classes="label"),
                        Input(placeholder="8"),
                        classes="column padwidthonly"),
                    Vertical(
                        Labels(" HP (1 to 10)", classes="label"),
                        Input(placeholder="7"),
                        classes="column padwidthonly"),
                    Vertical(
                        Labels(" Global offset", classes="label"),
                        Input(placeholder="Example: -10"),
                        classes="column padwidthonly"),
                ),
                Vertical(
                    Labels(" Creator name", classes="label"),
                    Input(placeholder="Example: bobermilk"),
                    classes="padwidthonly"),
                Vertical(
                    Labels(" Additional search tags", classes="label"),
                    Input(placeholder="Example: first_convert pizza lemon"),
                    classes="padwidthonly"),
                Horizontal(
                    Static("   Remove short lns                            ", classes="btnLabel"),
                    Switch(value=True),
                    classes="container",
                ),
                classes="column",
            ),
            Vertical(
                SectionTitle(f"Map rates (calc v{util.calc_version})"),
                Static(),
                Horizontal(
                    Vertical(
                        Labels(" Lowest rate (0.8 min)", classes="label"),
                        Input(placeholder="Example: 0.8"),
                        classes="column padwidthonly"),
                    Vertical(
                        Labels(" Highest rate (1.45 max)", classes="label"),
                        Input(placeholder="Example: 1.35"),
                        classes="column padwidthonly"),
                ),
                Vertical(
                    Labels(" Maximum msd for rates (1MSD to 100MSD)", classes="label"),
                    Input(placeholder="Example: 28.42"),
                    classes="column padwidthonly"),
                Horizontal(
                    Static("   Show skillset msd in diff names             ", classes="btnLabel"),
                    Switch(value=False),
                    classes="container",
                ),
                Horizontal(
                    Static("   Keep audio pitch for rates                  ", classes="btnLabel"),
                    Switch(value=True),
                    classes="container",
                ),
                classes="column",
            ),
        ),
        Button("Continue", variant="primary"),
        Static(),
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        global OD, HP, offset, creator, rates, remove_ln, diff_name_skillset_msd, additional_tags, keep_pitch
        # clear_note(self.app)
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
            user_offset=inputs[2]
            if not user_offset:
                user_offset=0
            else:
                user_offset=user_offset.lstrip("-")
                if user_offset.isdigit():
                    user_offset=int(user_offset)
                    if user_offset in range(-1000,1001):
                        global offset
                        offset+=user_offset
                    else:
                        notification_text+="\n"
                        notification_text+="    - User offset too large, (max 1000 milliseconds)"
                        fail=True
                        user_offset=0
                else:
                    user_offset=0
        except:
            user_offset=0

        log_text+="\n"
        log_text+=f"Warning: {user_offset} milliseconds will be applied to all converted maps"
        try:
            creator=str(inputs[3]).strip()
        except:
            log_text+="\n"
            log_text+="Invalid creator, defaulting to bobermilk"
            creator="bobermilk"
        if not creator:
            log_text+="\n"
            log_text+="Invalid creator, defaulting to bobermilk"
            creator="bobermilk"

        try:
            additional_tags=str(inputs[4]).strip()
        except:
            log_text+="\n"
            log_text+="Invalid additional tags, no additional tags will be added"
        if not creator:
            log_text+="\n"
            log_text+="No additional tags specified, no additional tags will be added"

        unspecified_rate_initial=False
        unspecified_rate_increment=False
        try:
            initial_rate=float(inputs[5])
        except:
            if not inputs[5].strip():
                unspecified_rate_increment=True
            log_text+="\n"
            log_text+="Warning: Invalid initial rate rate, defaulting to 1.0"
            initial_rate=1.0
        if initial_rate<0.8:
            notification_text+="\n"
            notification_text+="    - Initial rate out of bounds, please retry with a value in range 0.8 to 1.0"
            fail=True
        rates[0]=initial_rate

        try:
            rate_increment=float(inputs[6])
        except:
            if not inputs[6].strip():
                unspecified_rate_initial=True
            log_text+="\n"
            log_text+="Warning: Invalid rate increment, defaulting to 0.1"
            rate_increment=0.1
        if rate_increment<0.05 or rate_increment>0.1:
            notification_text+="\n"
            notification_text+="    - Rate increment out of bounds, please retry with a value in range 0.05 and 0.1"
            fail=True
        rates[1]=rate_increment

        try:
            rate_cnt=int(inputs[7])
        except:
            log_text+="\n"
            if not inputs[7].strip() and unspecified_rate_initial and unspecified_rate_increment:
                log_text+="Warning: no uprate options specified, not uprating anything."
                rate_cnt=1
            else:
                notification_text+="\n"
                notification_text+="    - Rate count has to be a integer greater than 0"
                fail=True
        if not rate_cnt>0:
            notification_text+="\n"
            notification_text+="    - Rate count has to be a integer greater than 0"
            fail=True
        rates[2]=rate_cnt

        unspecified_min_msd=False
        try:
            min_msd=float(inputs[8])
        except:
            if not inputs[8].strip():
                unspecified_min_msd=True
            log_text+="\n"
            log_text+="Warning: Invalid minimum msd, defaulting to no minimum msd limits"
            min_msd=-1.0
        if min_msd<1.0 or min_msd>100.0:
            notification_text+="\n"
            notification_text+="    - Minimum msd out of bounds, please retry with a value in range 1.0 and 100.0"
            fail=True
        msd_bounds[0]=min_msd

        try:
            max_msd=float(inputs[9])
        except:
            log_text+="\n"
            if not inputs[9].strip() and unspecified_min_msd:
                log_text+="Warning: no msd ranges specified, no msd bounds for uprates to be generated will be imposed"
                max_msd=-1
            else:
                notification_text+="\n"
                notification_text+="    - Maximum msd out of bounds, please retry with a value in range 1.0 and 100.0"
                fail=True

        if max_msd<1.0 or max_msd>100.0:
            notification_text+="\n"
            notification_text+="    - Maximum msd out of bounds, please retry with a value in range 1.0 and 100.0"
            fail=True
        rates[2]=max_msd

        if min_msd>max_msd:
            notification_text+="\n"
            notification_text+="    - Minimum msd cannot be greater than maximum msd!"
            fail=True

        buttons=[x.value for x in self.query(Switch)]
        remove_ln=buttons[0]
        if remove_ln:
            log_text+="\n"
            log_text+="Warning: Short LNs will be changed to normal note"
        else:
            log_text+="\n"
            log_text+="Warning: Short LNs will remain"

        show_skillset_msd=buttons[1]
        keep_pitch=buttons[2]
        if not keep_pitch:
            log_text+="\n"
            log_text+="Warning: Disabling keep audio pitch creates nightcore"

        if not notification_text=="Configuration Errors:":
            notify(self, notification_text)
        if not fail:
            if show_skillset_msd:
                body.mount(skillset_msd)
            else:
                self.app.exit(result=True)
            self.remove()


class SkillsetMsd(Container):
    def compose(self) -> ComposeResult:
        yield Vertical(
            SectionTitle("Select skillset MSD to be written into diff names"),
            Static(),
            Horizontal(
                Vertical(
                    Horizontal(
                        Static("    Stream    ", classes="btnLabel"),
                        Switch(value=True),
                        classes="container",
                    ),
                    Horizontal(
                        Static("    JumpStream", classes="btnLabel"),
                        Switch(value=True),
                        classes="container",
                    ),
                    Horizontal(
                        Static("    HandStream", classes="btnLabel"),
                        Switch(value=True),
                        classes="container",
                    ),
                    Horizontal(
                        Static("    Stamina   ", classes="btnLabel"),
                        Switch(value=True),
                        classes="container",
                    ),            

                classes="column"),
                Vertical(
                    Horizontal(
                        Static("    JackSpeed ", classes="btnLabel"),
                        Switch(value=True),
                        classes="container",
                    ),            
                    Horizontal(
                        Static("    ChordJack ", classes="btnLabel"),
                        Switch(value=True),
                        classes="container",
                    ),
                    Horizontal(
                        Static("    Technical ", classes="btnLabel"),
                        Switch(value=True),
                        classes="container",
                    ),
                classes="column"),
            ),
            Button("Continue", variant="primary"),
        )
    def on_button_pressed(self, event: Button.Pressed) -> None:
        global diff_name_skillset_msd
        diff_name_skillset_msd=[x.value for x in self.query(Switch)]
        self.app.exit(result=True)


# LinearLayout (https://textual.textualize.io/guide/layout/)
body=Body()
welcome=Welcome()
configuration=ChartAttributes()
skillset_msd=SkillsetMsd()

class etterna2osu(App):
    CSS_PATH = "gui.css"
    BINDINGS = [("ctrl+d", "toggle_dark", "Toggle dark mode"),
        ("ctrl+c", "app.quit", "Quit"),
        # ("f1", "app.toggle_class('TextLog', '-hidden')", "Recent Logs"),
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
    tui_result=app.run()
    try:
        if tui_result:
            util.main(OD, HP, offset, creator, additional_tags, rates, msd_bounds, remove_ln, diff_name_skillset_msd, keep_pitch)
    except:
        pass

