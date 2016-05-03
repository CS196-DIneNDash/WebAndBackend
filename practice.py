from firebase import firebase
from flask import Flask, request
app = Flask(__name__)



#adds meetup to database
# def addMeetup(location, time, maxPpl):
@app.route("/addMeetup/", methods = ['GET'])
def addMeetup():
	
	print str(request)
	location = request.args.get('location')
	location = location.replace("%22", "")
	location = location.replace('"', "")
	location = str(location)
	print (location)

	time = request.args.get('time')
	time = time.replace("%22", "")
	time = time.replace('"', "")
	time = str(time)
	print (time)

	maxPpl = request.args.get('maxPpl')
	maxPpl = maxPpl.replace("%22", "")
	maxPpl = maxPpl.replace('"', "")
	maxPpl = str(maxPpl)
	print (maxPpl)

	
	eventNum = findEventNumber(location, time)
	name = location + ' @ ' + time  + ', Group: ' + str(eventNum)

	return fb.put('/meetups/', name, {'Location': location, 'Time': time, "Max People": maxPpl, 'Event Number': eventNum, "Current People": 1, "Attending": {"User 1": 'Me'}})


#deletes meetup from database
# def deleteMeetup(location, time, eventNum):
@app.route("/deleteMeetup/", methods = ['GET'])
def deleteMeetup():
	print str(request)
	location = request.args.get('location')
	location = location.replace("%22", "")
	location = location.replace('"', "")
	location = str(location)
	print (location)

	time = request.args.get('time')
	time = time.replace("%22", "")
	time = time.replace('"', "")
	time = str(time)
	print (time)

	eventNum = request.args.get('eventNum')
	eventNum = eventNum.replace("%22", "")
	eventNum = eventNum.replace('"', "")
	eventNum = int(eventNum)
	print (eventNum)

	name = location + ' @ ' + time  + ', Group: ' + str(eventNum)
	return fb.delete('/meetups/', name)

#accesses meetup info
# def getMeetup(location, time, val):
@app.route("/getMeetup/", methods = ['GET'])
def getMeetup():
	print str(request)
	location = request.args.get('location')
	location = location.replace("%22", "")
	location = location.replace('"', "")
	location = str(location)
	print (location)

	time = request.args.get('time')
	time = time.replace("%22", "")
	time = time.replace('"', "")
	time = str(time)
	print (time)

	val = request.args.get('val')
	val = val.replace("%22", "")
	val = val.replace('"', "")
	val = str(val)
	print (val)

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

# def addMeetupMember(location, time, eventNum, newMember):
@app.route("/addMeetupMember/", methods = ['GET'])
def addMeetupMember():
	print str(request)
	location = request.args.get('location')
	location = location.replace("%22", "")
	location = location.replace('"', "")
	location = str(location)
	print (location)

	time = request.args.get('time')
	time = time.replace("%22", "")
	time = time.replace('"', "")
	time = str(time)
	print (time)

	eventNum = request.args.get('eventNum')
	eventNum = eventNum.replace("%22", "")
	eventNum = eventNum.replace('"', "")
	eventNum = int(eventNum)
	print (eventNum)

	newMember = request.args.get('newMember')
	newMember = newMember.replace("%22", "")
	newMember = newMember.replace('"', "")
	newMember = str(newMember)
	print (newMember)

	name = location + ' @ ' + time  + ', Group: ' + str(eventNum)
	currentPpl = fb.get('/meetups/'+name+"/Current People", None)
	maxPpl = fb.get('/meetups/'+name+"/Max People", None)

	if(currentPpl < maxPpl):
		currentState = getMeetup(location, time, eventNum)
		currentState['Attending']['User '+str(currentPpl+1)] = newMember
		currentState['Current People'] = currentPpl+1
		return fb.put('/meetups/', name, currentState)
	else:
		return "List Is Full"

# def getPlannedMeetup(location, time, eventNum, user):
@app.route("/getPlannedMeetup/", methods = ['GET'])
def getPlannedMeetup():

	print str(request)
	user = request.args.get('user')
	user = user.replace("%22", "")
	user = user.replace('"', "")
	user = str(user)
	print user

	return fb.get('/plannedMeetups/', user)

# def addToPlannedMeetups(location, time, eventNum, user):
@app.route("/addToPlannedMeetups/", methods = ['GET'])
def addToPlannedMeetups():

	print str(request)
	location = request.args.get('location')
	location = location.replace("%22", "")
	location = location.replace('"', "")
	location = str(location)
	print (location)

	time = request.args.get('time')
	time = time.replace("%22", "")
	time = time.replace('"', "")
	time = str(time)
	print (time)

	eventNum = request.args.get('eventNum')
	eventNum = eventNum.replace("%22", "")
	eventNum = eventNum.replace('"', "")
	eventNum = int(eventNum)
	print (eventNum)

	user = request.args.get('user')
	user = user.replace("%22", "")
	user = user.replace('"', "")
	user = str(user)
	print (user)

	check = fb.get('/plannedMeetups/'+user,None)
	print(check)
	print "oh yes"
	name = location + " @ " + time
	if check is None:
		fb.put('/plannedMeetups/', user, {name:{'Location': location, 'Time': time,  'Event Number': eventNum}})
		return check

	else:
		check[name] = {'Location': location, 'Time': time,  'Event Number': eventNum}

		fb.put('/plannedMeetups/', user,check)
		print('return flaws')
		return check
	print "over this"
	# return "this works"

if __name__ == "__main__":
    #port = int(os.environ.get('PORT', 5000))
    #app.run(host='0.0.0.0', port=port, debug = True)
    auth = firebase.FirebaseAuthentication('Nk9xiLFTq805hS9Sgid9RuCKAsIE8hJqhHYVP2uS', 'cs196BGE@gmail.com', True, True)
    fb = firebase.FirebaseApplication("https://brilliant-heat-3299.firebaseio.com/", auth)
    #print(addMeetupMember("Arby's", "4:00", 2, 'Harshit'))
    app.run(debug = True)
    


	
	# print(addMeetup("Arby's" , '5:00', 5))