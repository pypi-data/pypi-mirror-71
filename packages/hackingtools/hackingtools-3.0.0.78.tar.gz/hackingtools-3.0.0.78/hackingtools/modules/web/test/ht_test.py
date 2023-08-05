from hackingtools.core import Logger, Utils, Config
if Utils.amIdjango(__name__):
	from .library.core import hackingtools as ht
else:
	import hackingtools as ht
import os

config = Config.getConfig(parentKey='modules', key='ht_test')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():

	def __init__(self):
		self._main_gui_func_ = 'hola'

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_test'), debug_module=True)

	def hola(self, mensaje):
		return 'hola que tal, {m}'.format(m=mensaje)