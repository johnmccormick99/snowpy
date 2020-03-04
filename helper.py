import requests, json
import datetime
import sys

class ServiceNow:

	def __init__(self, chg=''):
		self.baseurl = 'https://dev94652.service-now.com/api/now'
		self.username = 'admin'
		self.password = 'LondonThursday123!'
		self.payload = ''
		self.headers = ''
		self.sysId = ''
		self.chg = chg
		self.headers = {"Content-Type":"application/json", "Accept":"application/json"}
		self.session = requests.Session()

	def loopkupChangeRequest(self) :

		if( self.chg == '') :
			sys.exit(-1)
			
		response = self.session.get(self.baseurl + '/table/change_request?sysparm_query=number=' + self.chg, 
		                            auth=(self.username, self.password), 
		                            headers=self.headers)

		if response.status_code != 200: 
			print('Status:', response.status_code)
			sys.exit(-1)

		self.sysId = json.loads( response.content.decode("UTF-8"))['result'][0]['sys_id']
		
		return( self.sysId )

	def approvedState(self) :
			
		response = self.session.get(self.baseurl + '/table/change_request?sys_id=' + self.sysId, 
		                            auth=(self.username, self.password), 
		                            headers=self.headers)

		if response.status_code != 200: 
			print('Status:', response.status_code)
			sys.exit(-1)

		state = json.loads( response.content.decode("UTF-8"))['result'][0]['state']
		dictionary = {'4' : 'Canceled', '3' : 'Closed', '0' : 'Review', '-1' : 'Implement', '-2' : 'Scheduled', '-3' : 'Authorize', '-4' : 'Assess', '-5' : 'New'}

		return ( dictionary[str(state)] )

	def isChangeWindowOpen(self) :
			
		response = self.session.get(self.baseurl + '/table/change_request?sys_id=' + self.sysId,
									auth=(self.username, self.password), 
									headers=self.headers)

		if response.status_code != 200: 
			print('Status:', response.status_code)
			sys.exit(-1)
		
		try:
			change_type  = json.loads( response.content.decode("UTF-8"))['result'][0]['type']
			start_time   = json.loads( response.content.decode("UTF-8"))['result'][0]['start_date']
			end_time     = json.loads( response.content.decode("UTF-8"))['result'][0]['end_date']
			assigned_to  = json.loads( response.content.decode("UTF-8"))['result'][0]['assigned_to']

			response = self.session.get(self.baseurl + '/table/sys_user/' + assigned_to['value'],
											auth=(self.username, self.password), 
											headers=self.headers)

			assigned_user = json.loads( response.content.decode("UTF-8"))['result']['name']
		except Exception:
			print("Change request fields not populated")
			sys.exit(-1)

		now   = datetime.datetime.now()
		start = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
		end   = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')

		if now > start and now < end:
			return {'change_windowopen': True, 'change_type': change_type, 'assigned_user': assigned_user }
		else:
			return {'change_windowopen': False, 'change_type': change_type, 'assigned_user': assigned_user }

	def addWorkNotes(self, notes) :

		response = self.session.put(self.baseurl + '/table/change_request/' + self.sysId, 
		                            auth=(self.username, self.password), 
		                            data=json.dumps({"work_notes":notes}), 
		                            headers=self.headers)
	
		if response.status_code != 200: 
			print('Status:', response.status_code)
			sys.exit(-1)
