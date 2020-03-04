import sys
from helper import ServiceNow

def main(argv):
	changenumber = argv[0]
	user = argv[1]
	obj = ServiceNow(changenumber)
	obj.loopkupChangeRequest()
	change_window  = obj.isChangeWindowOpen()
	approval_state = obj.approvedState()

	if change_window['assigned_user'] == user:
		print('ServiceNow Check - Passed: User is assigned to the change')
	else:
		print('ServiceNow Check - Failed: User is not assigned to the change')
		sys.exit(-1)

	if change_window['change_windowopen'] == True:
		print('ServiceNow Check - Passed: Change window is open')
	else:
		print('ServiceNow Check - Failed: Not within change window')
		sys.exit(-1)

	if change_window['change_type'] == 'emergency':
		print('ServiceNow Check - Passed: Emergency change ready to implement')
	elif change_window['change_type'] == 'normal' and approval_state == 'Implement' :
		print('ServiceNow Check - Passed: Ready to implement')
	else:
		print('ServiceNow Check - Failed: Not ready to implement')
		sys.exit(-1)

if __name__ == "__main__":
   main(sys.argv[1:])