import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib, Gdk, Gio
import gettext, locale, os, json, time

__version__ = "0.1.0"
APP_ID = "se.danielnylander.samtalsstod"
LOCALE_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'share', 'locale')
if not os.path.isdir(LOCALE_DIR): LOCALE_DIR = "/usr/share/locale"
try:
    locale.bindtextdomain(APP_ID, LOCALE_DIR)
    gettext.bindtextdomain(APP_ID, LOCALE_DIR)
    gettext.textdomain(APP_ID)
except Exception: pass
_ = gettext.gettext
def N_(s): return s


CARDS = [
    {"name": N_("My Turn"), "icon": "🗣️", "desc": N_("It is my turn to talk now")},
    {"name": N_("Your Turn"), "icon": "👂", "desc": N_("It is your turn to talk now")},
    {"name": N_("Wait"), "icon": "✋", "desc": N_("Please wait, I am thinking")},
    {"name": N_("I Don't Understand"), "icon": "❓", "desc": N_("Can you explain again?")},
    {"name": N_("Too Loud"), "icon": "🔇", "desc": N_("It is too loud for me")},
    {"name": N_("Break"), "icon": "⏸️", "desc": N_("I need a break")},
    {"name": N_("Yes"), "icon": "✅", "desc": N_("Yes, I agree")},
    {"name": N_("No"), "icon": "❌", "desc": N_("No, I don't want that")},
    {"name": N_("Help"), "icon": "🆘", "desc": N_("I need help")},
    {"name": N_("Happy"), "icon": "😊", "desc": N_("I feel happy right now")},
    {"name": N_("Sad"), "icon": "😢", "desc": N_("I feel sad right now")},
    {"name": N_("Thank You"), "icon": "🙏", "desc": N_("Thank you!")},
]

class MainWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title(_('Conversation Support'))
        self.set_default_size(550, 550)
        
        header = Adw.HeaderBar()
        menu_btn = Gtk.MenuButton(icon_name='open-menu-symbolic')
        menu = Gio.Menu()
        menu.append(_('About'), 'app.about')
        menu_btn.set_menu_model(menu)
        header.pack_end(menu_btn)
        
        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        main.append(header)
        
        self._display = Gtk.Label(label=_('Tap a card to show it'))
        self._display.add_css_class('title-1')
        self._display.set_margin_top(24)
        self._display.set_margin_bottom(8)
        main.append(self._display)
        
        self._desc = Gtk.Label()
        self._desc.add_css_class('title-4')
        self._desc.add_css_class('dim-label')
        self._desc.set_margin_bottom(16)
        main.append(self._desc)
        
        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(True)
        grid = Gtk.FlowBox()
        grid.set_max_children_per_line(3)
        grid.set_min_children_per_line(3)
        grid.set_selection_mode(Gtk.SelectionMode.NONE)
        grid.set_homogeneous(True)
        grid.set_row_spacing(8)
        grid.set_column_spacing(8)
        grid.set_margin_start(16)
        grid.set_margin_end(16)
        grid.set_margin_bottom(16)
        
        for card in CARDS:
            btn = Gtk.Button()
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
            box.set_margin_top(12)
            box.set_margin_bottom(12)
            icon = Gtk.Label(label=card['icon'])
            icon.add_css_class('title-1')
            box.append(icon)
            name = Gtk.Label(label=_(card['name']))
            name.add_css_class('caption')
            box.append(name)
            btn.set_child(box)
            btn.add_css_class('card')
            btn.connect('clicked', self._show_card, card)
            grid.insert(btn, -1)
        
        scroll.set_child(grid)
        main.append(scroll)
        self.set_content(main)
    
    def _show_card(self, btn, card):
        self._display.set_text(f"{card['icon']}  {_(card['name'])}")
        self._desc.set_text(_(card['desc']))

class App(Adw.Application):
    def __init__(self):
        super().__init__(application_id='se.danielnylander.samtalsstod')
        self.connect('activate', self._on_activate)
        about = Gio.SimpleAction.new('about', None)
        about.connect('activate', self._on_about)
        self.add_action(about)
    def _on_activate(self, app):
        MainWindow(application=app).present()
    def _on_about(self, a, p):
        Adw.AboutDialog(application_name=_('Conversation Support'), application_icon=APP_ID,
            version=__version__, developer_name='Daniel Nylander',
            website='https://github.com/yeager/samtalsstod',
            license_type=Gtk.License.GPL_3_0,
            comments=_('Visual conversation support cards'),
            developers=['Daniel Nylander <daniel@danielnylander.se>']).present(self.get_active_window())


def main():
    app = App()
    app.run()

if __name__ == "__main__":
    main()
