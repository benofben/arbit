from threading import Thread

class testit(Thread):
	def __init__ (self,x):
		Thread.__init__(self)
		self.x = x
		self.fx = -1
	def run(self):
		self.fx=self.x**self.x
		
threadList = []

for x in range(0,10):
	current = testit(x)
	threadList.append(current)
	current.start()

for thread in threadList:
	thread.join()
	print("Answer is ", thread.fx)
