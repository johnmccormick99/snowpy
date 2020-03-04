
import requests, json
import base64
import datetime
import math

class ServiceNow:

	def __init__(self, chg=''):
		self.baseurl = 'https://dev94652.service-now.com/api/now'
		self.username = 'admin'
		self.password = 'xxx'
		self.payload = ''
		self.headers = ''
		self.sysId = ''
		self.chg = chg
		self.headers = {"Content-Type":"application/json", "Accept":"application/json"}
		self.session = requests.Session()

	def loopkupChangeRequest(self, chg) :

		if( chg == '') :
			exit()
		
		self.chg = chg
			
		response = self.session.get(self.baseurl + '/table/change_request?sysparm_query=number=' + self.chg, 
		                            auth=(self.username, self.password), 
		                            headers=self.headers)

		if response.status_code != 200: 
			print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
			exit()

		self.sysId = json.loads( response.content.decode("UTF-8"))['result'][0]['sys_id']
		return( self.sysId )

	def approvedState(self) :
			
		response = self.session.get(self.baseurl + '/table/change_request?sys_id=' + self.sysId, 
		                            auth=(self.username, self.password), 
		                            headers=self.headers)

		if response.status_code != 200: 
			print('Status:', response.status_code, 
			      'Headers:', response.headers, 
			      'Error Response:',response.json())
			exit()

		self.state = json.loads( response.content.decode("UTF-8"))['result'][0]['state']
		return( int(self.state) )

	def isChangeWindowOpen(self) :
			
		response = self.session.get(self.baseurl + '/table/change_request?sys_id=' + self.sysId, auth=(self.username, self.password), headers=self.headers)

		if response.status_code != 200: 
			print('Status:', response.status_code, 
			      'Headers:', response.headers, 
			      'Error Response:',response.json())
			exit()

		start_time = json.loads( response.content.decode("UTF-8"))['result'][0]['start_date']
		end_time   = json.loads( response.content.decode("UTF-8"))['result'][0]['end_date']
		
		now   = datetime.datetime.now()
		start = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
		end   = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')

		if now > start and now < end:
			return True
		else:
			return False

	def addWorkNotes(self, notes) :

		response = self.session.put(self.baseurl + '/table/change_request/' + self.sysId, 
		                            auth=(self.username, self.password), 
		                            data=json.dumps({"work_notes":notes}), 
		                            headers=self.headers)
	
		if response.status_code != 200: 
			print('Status:', response.status_code, 
			      'Headers:', response.headers, 
			      'Error Response:',response.json())
			exit()
