from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, KeyChord
from libqtile.lazy import lazy
import re
import os
import subprocess

mod = "mod4"
terminal = "alacritty"

keys = [
    #volume control
    Key([],"XF86AudioRaiseVolume",lazy.spawn("amixer set Master 5%+"),desc="Raise volume"),
    Key([],"XF86AudioLowerVolume",lazy.spawn("amixer set Master 5%-"),desc="Lower volume"),
    
    #backlight control
    Key([],"XF86MonBrightnessUp",lazy.spawn("xbacklight -inc 10"),desc="increase backlight"),
    Key([],"XF86MonBrightnessDown",lazy.spawn("xbacklight -dec 10"),desc="decrease backlight"),
    
    #script
    Key([mod], "w", lazy.spawn("/home/wzj/rofi_scripts/wallpaper_switcher"),desc="select wallpaper"),
    Key([mod, "shift"], "n", lazy.spawn("/home/wzj/rofi_scripts/group_unminimize_all.fish")),
    Key([mod, "shift"], "m", lazy.spawn("/home/wzj/rofi_scripts/video_selector"),desc="select video"),
    Key([mod, "shift"], "q", lazy.spawn("/home/wzj/.config/qtile/powermenu.sh"), desc="launch powermenu"),
    Key([mod, "shift"], "w", lazy.spawn("/home/wzj/rofi_scripts/group_caster.fish"), desc="cast chosen group to screen"),
    Key([mod, "shift"], "p", lazy.spawn("/home/wzj/rofi_scripts/pdf_selector"),desc="view chosen pdf"),
    Key([mod], "s", lazy.spawn("/home/wzj/rofi_scripts/rofi_maim"),desc="screen shot in your preferred way"),
    Key([mod, "shift"], "s", lazy.spawn("/home/wzj/rofi_scripts/image_view"),desc="view pictures in ~/Pictures directory"),

    #software or built-bin widget
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "Return", lazy.spawn("tabbed "+terminal+" --embed"), desc="Launch terminal"),
    Key([mod, "shift"], "v",lazy.spawn("qv2ray"),desc="proxy"),
    Key([mod], "v",lazy.spawn("code"),desc="vscode"),
    Key([mod],"e",lazy.spawn("emacsclient -c -a 'emacs'"),desc="Launch my emacs"),
    Key([mod],"c",lazy.spawn("copyq toggle"),desc="open clipboard"),
    Key([mod],"p",lazy.spawn("rofi -show run"),desc="run commands"),
    Key([mod,"shift"],"d",lazy.spawn("rofi -show drun"),desc="run apps"),
    Key([mod], "o", lazy.spawn("feeluown"),desc="open music player"),
    # Key([mod],"b",lazy.spawn("qutebrowser"),desc="run minimal browser"),
    Key([mod],"b",lazy.spawn("nyxt"),desc="run minimal browser"),
    Key([mod,"shift"],"b",lazy.spawn("firefox-developer-edition"),desc="run max browser"),

    #focus control
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    
    #window movement
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    #window special actions control
    Key([mod], "equal", lazy.layout.grow(), desc="Grow in size"),
    Key([mod], "minus", lazy.layout.shrink(), desc="Decrease in size"),
    Key([mod], "m", lazy.window.toggle_maximize(), desc="Maximze main window sizes"),
    Key([mod], "n", lazy.window.toggle_minimize(), desc="hide my window"),
    Key([mod,"shift"], "space", lazy.window.toggle_floating(),desc="Toggle floating"),
    Key([mod,"shift"], "f", lazy.window.toggle_fullscreen(),desc="Toggle fullscreen"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    
    #stack layout control
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),

    # Toggle between different layouts as defined below
    Key([mod,"shift"], "period", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod,"shift"], "comma", lazy.prev_layout(), desc="Toggle between layouts"),

    #group display control
    Key([mod], "period", lazy.screen.next_group(), desc="focus next group"),
    Key([mod], "comma", lazy.screen.prev_group(), desc="focus previous group"),

    #window manager control
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
]

groups = [Group("1",label="",layout="monadtall"),
          Group("2",label="",layout="monadtall",matches=[Match(wm_class=["qutebrowser","nyxt","firefox-developer-edition"])]),
          Group("3",label="",layout="floating",matches=[Match(wm_class=["chimera","PyMOL","tk"])]),
          Group("4",label="",layout="monadtall",matches=[Match(wm_class=["Zathura"])]),
          Group("5",label="",layout="monadtall",matches=[Match(wm_class=["code","neovide","emacs"])]),
          Group("6",label="",layout="max",matches=[Match(wm_class=["mpv","feeluown","feh","sxiv","gimp-2.10"])]),
          Group("7",label="",layout="floating",matches=[Match(wm_class=["VirtualBox Manager"])]),
          Group("8",label="",layout="floating",matches=[Match(wm_class=["Wine"])]),
          Group("9",label="",layout="max",matches=[Match(wm_class=["libreoffice"])])]

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
    layout.MonadTall(margin=5,border_width=4),
    #layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Max(),
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    layout.Matrix(margin=5,border_width=4),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="SourceCodePro",
    fontsize=13,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    background="#f0f8ff",
                    block_highlight_text_color="#cc0000",
                    highlight_method="border",
                    active="#a2a2d0",
                    hide_unused=True,
                    ),
                widget.TextBox("",
                    fontsize=64,
                    background="#a4c639",
                    padding=-13,
                    foreground="#f0f8ff"
                    ),
                widget.CurrentLayout(
                    background="#a4c639",
                    foreground="#e32636"
                    ),
                widget.TextBox("",
                    fontsize=64,
                    background="#f0f8ff",
                    padding=-13,
                    foreground="#a4c639"
                    ),
                widget.TaskList(
                    highlight_method="block",
                    border="#fae7b5",
                    markup_focused="{}",
                    markup_floating="{}",
                    markup_maximized="{}",
                    background="#f0f8ff",
                    foreground="#4b5320",
                    unfocused_border='#bcd4e6',
                    spacing=3,
                    ),
                widget.TextBox("",
                    fontsize=64,
                    background="#f0f8ff",
                    padding=-13,
                    foreground="#a4c639"
                    ),
                widget.Prompt(
                    background="#a4c639",
                    foreground="#e32636"
                    ),
                widget.TextBox("",
                    fontsize=64,
                    background="#a4c639",
                    padding=-13,
                    foreground="#f0f8ff"
                    ),
                widget.Chord(
                    background="#f0f8ff",
                    chords_colors={
                        "launch": ("#e9d66b", "#ffbff0"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.TextBox("",
                    fontsize=64,
                    background="#f0f8ff",
                    padding=-13,
                    foreground="#a4c639"
                    ),
                widget.TextBox("",
                    fontsize=25,
                    background="#a4c639"
                    ),
                widget.Battery(
                    charge_char="",
                    discharge_char="",
                    full_char="",
                    format="{char}{percent:2.0%}",
                    foreground="#e32636",
                    background="#a4c639"
                    ),
                widget.TextBox("",
                    fontsize=64,
                    background="#a4c639",
                    padding=-13,
                    foreground="#f0f8ff"
                    ),
                widget.Clock(
                    foreground="#4b5320",
                    background="#f0f8ff",
                    format=" %Y-%m-%d %a %I:%M %p"
                    ),
                widget.TextBox("",
                    fontsize=64,
                    background="#f0f8ff",
                    padding=-13,
                    foreground="#a4c639"
                    ),
                widget.Systray(
                    background="#a4c639"
                    ),
            ],
            24,
            border_width=[2, 2, 2, 2],  # Draw top and bottom borders
            border_color=["#5d8aa8", "#5d8aa8", "#5d8aa8", "#5d8aa8"],  # Borders are magenta
            margin=[6,4,4,6]
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
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

@hook.subscribe.startup_once
def start_once():
    os.system('/home/wzj/.config/qtile/autostart.sh')
# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
