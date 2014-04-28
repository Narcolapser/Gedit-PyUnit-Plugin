####################################################################################################
#	Program:	Gedit Python Unit Test running script
#	Programmer:	Toben "Narcolapser" Archer
#	Date:		2014/04/26
#	Version:	0.1
#	Purpose:	To integrate gedit into a python test driven development enviorment, further
#		extending my use of gedit as an IDE.
#################################################

#TODO:
#	Re-create the testing system so that we don't have to reroute stderr to get results.
#	Multi thread the test process so that gedit stays responsive.
#	Maybe better format the output. we'll see.
#	Configuration management so that the plugin can be easily altered to user specific work flow
#		perhaps have a simple pop up or something in the status bar so the bottom panel
#		doesn't have to be open to see if the program passed it's tests or not.
#	Know that if you are in "test_vector.py" you should be running "test_vector.py" against 
#		"vector.py" and not "test_test_vectory.py" against "test_vector.py"

from gi.repository import GLib, Gio, GObject, Gtk, Gedit, PeasGtk
import inspect
import subprocess

# Bug 668924 - Make gedit_debug_message() introspectable <https://bugzilla.gnome.org/show_bug.cgi?id=668924>
try:
	debug_plugin_message = Gedit.debug_plugin_message
except:
	def debug_plugin_message(format_str, *format_args):
		filename, lineno, func_name = get_trace_info(1)
		Gedit.debug(Gedit.DebugSection.DEBUG_PLUGINS, filename, lineno, func_name)


class PyUnitPlugin(GObject.Object, 
		Gedit.ViewActivatable, PeasGtk.Configurable):
	__gtype_name__ = "PyTest"
#	settings = Gio.Settings.new("org.gnome.gedit.plugins.PyTest")
	view = GObject.property(type = Gedit.View)
	window = GObject.property(type=Gedit.Window)

	def __init__(self):
		GObject.Object.__init__(self)

		debug_plugin_message("self = %r", self)

	def __del__(self):
		debug_plugin_message("self = %r", self)

	def do_activate(self):
		"""Connect to the document's 'saved' signals."""
		doc = self.view.get_buffer()

		if not hasattr(doc, "saved_handler_id"):
			doc.saved_handler_id = doc.connect("saved", self.__on_document_saved)
		
		#Prepare the output panel.
		self.ga = Gedit.App.get_default()
		self.window = self.ga.get_active_window()
		self.iconPassed = Gtk.Image.new_from_stock(Gtk.STOCK_YES, Gtk.IconSize.MENU)
		self.iconFailed = Gtk.Image.new_from_stock(Gtk.STOCK_STOP, Gtk.IconSize.MENU)
		self.output_label = Gtk.Label('Results form PyUnit will display here.')
		self.panel = self.window.get_bottom_panel()
		self.panel.add_item(self.output_label,
			"PyUnitResultsPanel", "PyUnit Results", self.iconFailed)

	def do_deactivate(self):
		"""Disconnect from the document's 'saved' signals."""
		doc = self.view.get_buffer()

		try:
			saved_handler_id = doc.saved_handler_id
		except AttributeError:
			pass
		else:
			del doc.saved_handler_id
			doc.disconnect(saved_handler_id)

	def __on_document_saved(self, doc, err):
		fileLocation = doc.get_location().get_path()
		fileName = fileLocation[1+fileLocation.rindex('/'):]
		filePath = fileLocation[:fileLocation.rindex('/')+1]
		moduleName = fileName[:fileName.index('.py')]
		try:
			res = subprocess.check_output('python "' + filePath+'test_'+fileName + '" 2>&1',shell=True)
			if not isinstance(res,str):
				res = res.decode('utf-8')
		except Exception as e:
			res = 'testing did not happen: ' + str(e)
		
		self.__update_panel(Gtk.Label(res),True)
	
	def __update_panel(self,newLabel,status):
		self.panel.remove_item(self.output_label)
		self.output_label = newLabel
		if status:
			self.panel.add_item(self.output_label,
				"PyUnitResultsPanel", "PyUnit Results", self.iconPassed)
		else:
			self.panel.add_item(self.output_label,
				"PyUnitResultsPanel", "PyUnit Results", self.iconFailed)
		
		self.panel.activate_item(self.output_label)
