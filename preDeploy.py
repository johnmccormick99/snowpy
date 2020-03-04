import sys
from helper import ServiceNow

def main(argv):

	changenumber = argv
	obj = ServiceNow(changenumber)
	obj.loopkupChangeRequest(changenumber)

	if obj.approvedState() == 'Implement':
		print('Passed: Ready to implement')
	else:
		print('Failed: Not ready to implement')

	if obj.isChangeWindowOpen() == 'True':
		print('Passed: Change window open')
	else:
		print('Failed: Not within change window')

if __name__ == "__main__":
   main(sys.argv[1])
