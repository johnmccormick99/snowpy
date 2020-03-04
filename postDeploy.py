
from helper import ServiceNow

def main():

	chg = "CHG0040006"
	s = ServiceNow(chg)
	l = s.loopkupChangeRequest(chg)
	s.addWorkNotes("Meow!")

if __name__ == "__main__":
   main()
