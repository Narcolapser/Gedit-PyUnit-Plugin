####################################################################################################
#	Program:	Gedit Python Unit Test running script
#	Programmer:	Toben "Narcolapser" Archer
#	Date:		2014/04/26
#	Version:	0.1
#	Purpose:	To integrate gedit into a python test driven development enviorment, further
#		extending my use of gedit as an IDE.
#################################################

from gi.repository import GLib, Gio, GObject, Gtk, Gedit, PeasGtk
import inspect
import imp
import unittest
import traceback

# Bug 668924 - Make gedit_debug_message() introspectable <https://bugzilla.gnome.org/show_bug.cgi?id=668924>
try:
	debug_plugin_message = Gedit.debug_plugin_message
except:
	def debug_plugin_message(format_str, *format_args):
		filename, lineno, func_name = get_trace_info(1)
		Gedit.debug(Gedit.DebugSection.DEBUG_PLUGINS, filename, lineno, func_name)


class PyUnitPlugin(GObject.Object, Gedit.ViewActivatable, PeasGtk.Configurable):
	__gtype_name__ = "PyTest"
#	settings = Gio.Settings.new("org.gnome.gedit.plugins.PyTest")
	view = GObject.property(type = Gedit.View)

	def __init__(self):
		GObject.Object.__init__(self)
		
		#Prepare the output panel.
		self.ga = Gedit.App.get_default()
		self.window = self.ga.get_active_window()
		self.iconPassed = Gtk.Image.new_from_stock(Gtk.STOCK_YES, Gtk.IconSize.MENU)
		self.iconFailed = Gtk.Image.new_from_stock(Gtk.STOCK_STOP, Gtk.IconSize.MENU)
		self.output_label = Gtk.Label('Results form PyUnit will display here.')
		self.panel = self.window.get_bottom_panel()
		self.panel.add_item(self.output_label,
			"PyUnitResultsPanel", "PyUnit Results", self.iconFailed)

	def __del__(self):
		pass

	def do_activate(self):
		"""Connect to the document's 'saved' signals."""
		doc = self.view.get_buffer()

		if not hasattr(doc, "saved_handler_id"):
			doc.saved_handler_id = doc.connect("saved", self.__on_document_saved)
		



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
			module = self.__load_module(moduleName,filePath)
			suite = self.__load_suite(module)
			#results = unittest.Test_Result()
			#suite.run(results)
			#res = str(results)
			res = 'DONE!'
		except Exception as e:
			#res = 'testing did not happen: ' + str(e)
			res = traceback.print_exc()
		
		self.__update_panel(Gtk.Label(res),True)
	
	def __load_module(self,name,path):
		magic = imp.find_module(name,[path])
		module = imp.load_module(name,magic[0],magic[1],magic[2])
		return module
	
	def __load_suite(self,module):
		return unittest.TestLoader().loadTestsFromTestCase(self.__find_tests(module))
		
	def __find_tests(self,module):
		testCases = []
		for a in dir(module):
			if 'setUp' in dir(a):
				testCases.append(a)
		return testCases
	
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
