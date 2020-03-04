import sys
from helper import ServiceNow

def main(argv):

	changenumber = argv
	obj = ServiceNow(changenumber)
	obj.loopkupChangeRequest()
	obj.addWorkNotes("Deployment finished")

if __name__ == "__main__":
   main(sys.argv[1:])
