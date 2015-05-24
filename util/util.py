import os

def goToFileDir(file):
	print "Current directory:"
	print(os.getcwd())
	os.chdir(os.path.dirname(os.path.realpath(file)))
	print "Change to:"
	print(os.getcwd())