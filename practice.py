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


def addMeetupMember(location, time, eventNum, newMember):
	name = location + ' @ ' + time  + ', Group: ' + str(eventNum)
	currentPpl = fb.get('/meetups/'+name+"/Current People", None)
	maxPpl = fb.get('/meetups/'+name+"/Max People", None)
	# print (newMember)
	print (fb.get('/meetups/'+name+"/Max People", None))
	print str(currentPpl)

	if(currentPpl < maxPpl):
		currentState = getMeetup(location, time, eventNum)
		currentState['Attending']['User'+str(currentPpl+1)] = newMember
		currentState['Current People'] = currentPpl+1
		fb.put('/meetups/', name, currentState)

def getPlannedMeetup(location, time, eventNum, user):
	print fb.get('/plannedMeetups/', user)
	return fb.get('/plannedMeetups/', user)

def addToPlannedMeetups(location, time, eventNum, user):
	check = fb.get('/plannedMeetups/'+user,None)
	print(check)
	name = location + " @ " + time
	if check is None:
		return fb.put('/plannedMeetups/', user, {name:{'Location': location, 'Time': time,  'Event Number': eventNum}})
	else:
		check[name] = {'Location': location, 'Time': time,  'Event Number': eventNum}
		return fb.put('/plannedMeetups/', user,check)



auth = firebase.FirebaseAuthentication('Nk9xiLFTq805hS9Sgid9RuCKAsIE8hJqhHYVP2uS', 'cs196BGE@gmail.com', True, True)
fb = firebase.FirebaseApplication("https://brilliant-heat-3299.firebaseio.com/", auth)

addMeetupMember("Arby's", '4:00', 2, 'Sania')