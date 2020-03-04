import sys
from helper import ServiceNow

def main(argv):

	changenumber = argv
	obj = ServiceNow(changenumber)
	obj.loopkupChangeRequest(changenumber)
	change_window  = obj.isChangeWindowOpen()
	approval_state = obj.approvedState()

	if change_window['assigned_user'] == 'ITIL User':
		print('Passed: User is assigned to the change')
	else:
		print('Failed: User is not assigned to the change')
		#exit()

	if change_window['change_windowopen'] == True:
		print('Passed: Change window open')
	else:
		print('Failed: Not within change window')
		#exit()

	if change_window['change_type'] == 'emergency':
		print('Passed: Emergency change ready to implement')
	elif change_window['change_type'] == 'normal' and approval_state == 'Implement' :
		print('Passed: Ready to implement')
	else:
		print('Failed: Not ready to implement')
		#exit()

if __name__ == "__main__":
   main(sys.argv[1])