from firebase import firebase


#adds meetup to database
def addMeetup(location, time, maxPpl):
	
	eventNum = findEventNumber(location, time)
	name = location + ' @ ' + time  + ', Group: ' + str(eventNum)

	return fb.put('/meetups/', name, {'Location': location, 'Time': time, "Max People": maxPpl, 'Event Number': eventNum, "Current People": 1, "Attending": {"User 1": 'Me'}})


#deletes meetup from database
def deleteMeetup(location, time, eventNum):
	name = location + ' @ ' + time
	return fb.delete('/meetups/', name)

#accesses meetup info
def getMeetup(location, time, val):
	name = location + ' @ ' + time  + ', Group: ' + str(val)
	return fb.get('/meetups/', name)

# finds unique event number for identical
def findEventNumber(location, time):
	
	numberFound = False
	eventNum = 1

	while not numberFound:
		if getMeetup(location, time, eventNum) is None:
			print (eventNum)
			return eventNum
		else:
			eventNum+=1


auth = firebase.FirebaseAuthentication('Nk9xiLFTq805hS9Sgid9RuCKAsIE8hJqhHYVP2uS', 'cs196BGE@gmail.com', True, True)
fb = firebase.FirebaseApplication("https://brilliant-heat-3299.firebaseio.com/", auth)


print(addMeetup("Arby's", "4:00", 7))

# print(addMeetup("Arby's" , '5:00', 5))
