import sqlite3
from sqlite3 import Error
import datetime
from flask import Flask, render_template, redirect, request

app = Flask(__name__)

#Other function
def getLocalTime():
	time= datetime.datetime.now()
	time= str(time)
	return time[0:19]

#Sqlite query

#Create Table if don't exist.
#The name of Table: URL.
#The name of DB: Url.db.	
def createTable():
	conn = sqlite3.connect('Url.db',check_same_thread=False)
	cursor = conn.cursor()
	cursor.execute('CREATE TABLE IF NOT EXISTS URL (url TEXT PRIMARY KEY,Fakeurl TEXT)')
	cursor.execute('CREATE TABLE IF NOT EXISTS DATE (Date TEXT,Boolean TEXT)')
	conn.commit()
	conn.close()

def showAllRow():
	conn = sqlite3.connect('Url.db',check_same_thread=False)
	cursor = conn.cursor()
	cursor.execute("SELECT url,Fakeurl FROM URL")
	for url5,fakeURL in cursor.fetchall():
		print('['+url5+" , "+fakeURL+']')
	conn.close()

def RemoveAllRow():
	conn = sqlite3.connect('Url.db',check_same_thread=False)
	cursor = conn.cursor()
	cursor.execute("DELETE FROM URL")
	conn.commit()
	conn.close()

def CountRow():
	conn = sqlite3.connect('Url.db',check_same_thread=False)
	cursor = conn.cursor()
	cursor.execute("select count(*) from url") 
	count=cursor.fetchone()[0]
	return str(count)
	
# listStats The index mean 0-count url,if redirect suucces add here: 1-day 2-hour 3-minute ,else add here : 4-day 5-hour 6-minute	
def CalculateStats():
	listStats = [0, 0, 0, 0, 0, 0, 0]
	cuurentTime = getLocalTime()
	conn = sqlite3.connect('Url.db',check_same_thread=False)
	cursor = conn.cursor()
	cursor.execute("SELECT Date,Boolean FROM DATE")
	for tuple1 in cursor.fetchall():
		date = str(tuple1[0])
		state = str(tuple1[1])
		if state == "True":
			index = 1
		else:
			index = 4
		#check the redirection of day and hour and minute
		if cuurentTime[0:10] == date[0:10]:
			listStats[index] = 1 + listStats[index]
			if cuurentTime[11:13] == date[11:13]:
				listStats[index+1] = 1 + listStats[index+1]
				if cuurentTime[14:16] == date[14:16]:
					listStats[index+2] = 1 + listStats[index+2]
	conn.close()
	listStats[0] = CountRow()
	return listStats 


#App.route

#home page-default
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

#default for: /redirect/...
#serach real URL in the DB, and redirect to URL.
@app.route('/redirect/<string:string_url>')	
def redirectUrl(string_url):
	fakeurl1="localhost:5000/redirect/"+string_url
	conn = sqlite3.connect('Url.db',check_same_thread=False)
	cursor = conn.cursor()
	cursor.execute("SELECT url FROM URL WHERE Fakeurl=?",(fakeurl1,))
	realUrl = cursor.fetchone()
	#move Tuple to string
	try:
		realUrl=realUrl[0]
		cursor.execute("INSERT INTO DATE(Date,Boolean)VALUES(?,?)",(getLocalTime(),"True"))
		conn.commit()
		conn.close()
		return redirect(realUrl)
	except:
		cursor.execute("INSERT INTO DATE(Date,Boolean)VALUES(?,?)",(getLocalTime(),"False"))
		conn.commit()
		conn.close()
		return "<h1> Bad URL</h1>"
	

#Store the FakeUrl and real URL in the DB and send back Fakeurl to user.
#The createion of FakeUrl is done by the number of row in Table.
@app.route('/createURL',methods=['POST'])
def createURL():
	conn = sqlite3.connect('Url.db',check_same_thread=False)
	cursor = conn.cursor()
	#Get Url
	URL1 = request.form['URL']
	cursor.execute("SELECT url FROM URL WHERE url=?",(URL1,))
	check = cursor.fetchone()
	#The url exist in the DB
	if check != None:
		cursor.execute("SELECT Fakeurl FROM URL WHERE url=?",(URL1,))
		fakeurl = cursor.fetchone()
		#move Tuple to string
		fakeurl = fakeurl[0]
		conn.close()
		return render_template('home.html',fakeurl=fakeurl)
	#Create new row in table 	
	fakeurl = "localhost:5000/redirect/" + CountRow()
	cursor.execute("INSERT INTO URL(url,Fakeurl)VALUES(?,?)",(URL1, fakeurl))
	conn.commit()
	conn.close()
	return render_template('home.html',fakeurl=fakeurl)

@app.route('/stats')
def showStats():
	listStats = CalculateStats()	
	return render_template('stats.html',listStats=listStats)
			

if __name__=='__main__':
	createTable()
	app.run(debug = True)

