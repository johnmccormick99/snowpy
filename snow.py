
from helper import ServiceNow

def main():

	chg = "CHG0040006"
	s = ServiceNow(chg)
	l = s.loopkupChangeRequest(chg)
	print (l)
	a = s.approvedState()
	print (a)
	o = s.isChangeWindowOpen()
	print (o)
	s.addWorkNotes("Meow!")

if __name__ == "__main__":
   main()