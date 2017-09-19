import sys

class App():
	def __init__(self):
		self.exit_flag = False
		self.IGNORE_EXIT_FLAG = True

	def printflush(self, string, ignore_exit = False ):
		"""
		Print text and flush stdout
		"""
		if not self.getExitFlag() or ignore_exit == self.IGNORE_EXIT_FLAG:
			print str(string)
			sys.stdout.flush()
		
	def setExitFlag(self, exit_flag):
		self.exit_flag = exit_flag
		
	def getExitFlag(self):
		return self.exit_flag
		
	def deltaSeconds(self, delta):
		return float(delta.seconds) + float(delta.microseconds) / 1000000
	