import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

builder = Gtk.Builder()
builder.add_from_file("ejemplo1.glade")

handlers = { "onDeleteWindow": Gtk.main_quit }

builder.connect_signals(handlers)

window = builder.get_object("ventana_principal")

window.show_all()

Gtk.main()
