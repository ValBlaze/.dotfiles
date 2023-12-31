# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from floating_window_snapping import move_snap_window
from qtile_extras import widget
from qtile_extras.widget import decorations
from qtile_extras.widget.decorations import RectDecoration
import os
import subprocess

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.Popen([home])


mod = "mod4"
terminal = "kitty"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between QWndows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn("rofi -show drun -show-emojies"), desc="Spawn a command using a prompt widget"),
    # Sound
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -c 0 sset Master 1- unmute")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -c 0 sset Master 1+ unmute")),
    # Custom
    Key([mod], "f", lazy.window.toggle_fullscreen()),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    # layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    layout.Bsp(margin = [5, 5, 5, 5]),
    layout.Max(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

def open_pavu():
    qtile.cmd_spawn("pavucontrol")

# separator
def separator():
    return widget.Sep(
        foreground="0D0F18",
        padding=4,
        linewidth=3,
    )


def separator_sm():
    return widget.Sep(
        foreground="#0D0F18",
        padding=1,
        linewidth=1,
        size_percent=55,
    )

def _left_decor(color: str, padding_x=None, padding_y=4, round=False):
    radius = 4 if round else [4, 0, 0, 4]
    return [
        RectDecoration(
            colour=color,
            radius=radius,
            filled=True,
            padding_x=padding_x,
            padding_y=padding_y,
        )
    ]

def _right_decor(round=False):
    radius = 4 if round else [0, 4, 4, 0]
    return [
        RectDecoration(
            colour="#2C323C",
            radius=radius,
            filled=True,
            padding_y=4,
            padding_x=0,
        )
    ]

def separator():
    return widget.Sep(
        foreground="#292D3E",
        padding=4,
        linewidth=3,
    )

workspace_names = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
]

group_box_settings = {
    'active': "#bfc7d5",
    'block_highlight_text_color': "#bfc7d5",
    'this_current_screen_border': "#bfc7d5",
    'this_screen_border': "#bfc7d5",
    'urgent_border': "#ff5370",
    'background': "#292D3E",  # background is [10-12]
    'other_current_screen_border': "#bfc7d5",
    'other_screen_border': "#bfc7d5",
    'highlight_color': "#2C323C",
    'inactive': "#3E4452",
    'foreground': "#bfc7d5",
    'borderwidth': 2,  # change to 2 to add bottom border to active group
    'disable_drag': True,
    'fontsize': 20,
    'highlight_method': 'line',
    'padding_x': 10,
    'padding_y': 16,
    'rounded': False,
}

widget_defaults = dict(
    font="firacode nerd font",
    fontsize=15,
    padding=2,
    background="#292D3E",
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    font="firacode nerd font",
                    visible_groups=workspace_names,
                    ** group_box_settings,
                ),
                separator(),
                widget.Spacer(),
                widget.WindowName(
                    foreground="#bfc7d5",
                    width=bar.CALCULATED,
                    empty_group_string='Desktop',
                    max_chars=40,
                ),
                widget.Spacer(),
                widget.Systray(
                    padding=5,
                    icon_size=20,
                ),
                separator(),
                widget.CurrentLayoutIcon(
                    custom_icon_paths=[os.path.expanduser('~/.config/qtile/icons')],
                    scale=0.65,
                    use_mask=True,
                    foreground="#292D3E",
                    decorations=_left_decor("#FAE3B0"),
                ),
                separator_sm(),
                widget.CurrentLayout(
                    foreground="#FAE3B0",
                    padding=8,
                    decorations=_right_decor(),
                ),
                separator(),
                widget.TextBox(
                    fontsize=20,
                    text="墳",
                    padding=8,
                    foreground="#292D3E",
                    decorations=_left_decor("#90CEAA"),
                ),
                separator_sm(),
                widget.PulseVolume(
                    foreground="#90CEAA",
                    limit_max_volume='True',
                    mouse_callbacks={'Button3': open_pavu},
                    padding=8,
                    decorations=_right_decor(),
                ),
                separator(),
                widget.Wlan(
                    format="󰖩 ",
                    foreground="#292D3E",
                    disconnected_message="󰖪 ",
                    fontsize=16,
                    interface='wlp6s0',
                    update_interval=5,
                    # mouse_callbacks={
                        #'Button1': lambda: qtile.cmd_spawn('' + home + '/.local/bin/nmgui'),
                        # 'Button3': lambda: qtile.cmd_spawn(myTerm + ' -e nmtui'),
                    # },
                    padding=4,
                    decorations=_left_decor("#ff869a"),
                ),
                separator_sm(),
                widget.Wlan(
                    format='{percent:2.0%}',
                    foreground="#ff869a",
                    disconnected_message=' ',
                    interface='wlp6s0',
                    update_interval=5,
                    # mouse_callbacks={
                        # 'Button1': lambda: qtile.cmd_spawn('' + home + '/.local/bin/nmgui'),
                        # 'Button3': lambda: qtile.cmd_spawn(myTerm + ' -e nmtui'),
                    # },
                    padding=8,
                    decorations=_right_decor(),
                ),
                separator(),
                widget.TextBox(
                    text='',
                    fontsize=16,
                    foreground="#292D3E",
                    padding=8,
                    decorations=_left_decor("#82b1ff"),
                    # mouse_callbacks={'Button1': open_calendar},
                ),
                separator_sm(),
                widget.Clock(
                    format='%b %d, %I:%M %p',
                    foreground="#82b1ff",
                    padding=8,
                    decorations=_right_decor(),
                    # mouse_callbacks={'Button1': open_calendar},
                ),
            ],
            30,
            margin=[4, 6, 2, 6],
            border_width=[0, 0, 0, 0],
            border_color="#0D0F18",
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", move_snap_window(snap_dist=20), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = True
cursor_warp = True
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
