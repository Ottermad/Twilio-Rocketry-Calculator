from flask import Flask, request, redirect
import twilio.twiml
#import main_calc
import os
from flask.ext.sqlalchemy import SQLAlchemy
from main_calc import *

 
app = Flask(__name__)
'''
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://gzfputtxvzdxzq:ENBTQbGhYK_EdJO4f8y5eCr6m7@ec2-54-83-43-49.compute-1.amazonaws.com:5432/d3u902tfr1npfp"
db = SQLAlchemy(app)

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    var1 = db.Column(db.String(80))
   
    def __init__(self, var1):
        self.var1 = var1

    def __repr__(self):
        return self.var1

test = Test('250')
db.session.add(test)
db.session.commit()
all_tests = Test.query.all()
'''
 
#Sample data
def getRocketFromUserRequest(rockets,user_request):
    for rocket in rockets:
        if rocket == user_request:
            return rockets[rocket]
    #print "Rocket not found"
    return "Rocket not found"

def getMotorFromUserRequest(motors,user_request):
    for motor in motors:
        if motor == user_request:
            return motors[motor]
    #print "Motor not found"
    return "Motor not found"

motorA = Motor(7,6,5,4)
motorB = Motor(1,1,1,1)

rocketA = rocket(Component(1,1),NoseConeTypes.cone,Component(2,1),Component(3,1),motorB,Component(5,1),1,2,3,4,5,6,7,8,9,10,11,12,13,14)
rocketB = rocket(Component(1,1),NoseConeTypes.cone,Component(2,1),Component(3,1),motorB,Component(5,1),1,2,3,4,5,6,7,8,9,10,11,12,13,14)

motors = {
    "motorA":motorA,
    "motorB":motorB
}

rockets = {
    "rocketA":rocketA,
    "rocketB":rocketB
}



# Try adding your own number to this list!
callers = {
    "+447763501564": "Jordi",
    "+447804654075": "Thomas",
    "+447795958759": "Charles",
}
 
@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond and greet the caller by name."""


    body_message = str(request.values.get('Body', None))
    rocket_name = body_message.split(' ') [0]
    rocket_motor = body_message.split(' ') [1]

    currentMotor = getMotorFromUserRequest(motors,rocket_motor)
    currentRocket = getRocketFromUserRequest(rockets,rocket_name)

    #Create the users rocket
    currentRocket.engine = currentMotor

    
    from_number = request.values.get('From', None)
  
   #''' if from_number in callers:
    #    message = rocket_name + " has an altitude of " + str(currentRocket.altitude) + " m. "
     #   if (currentRocket.stability > 0):
      #      message = message + user_request_rocket + " is stable at: " + str(currentRocket.stability)
  #      else:
   #         message = message + "Don't fly, the rocket is unstable" 

    #else:
     #   message = "Good try! But you're not smart enough to use our application :) #MLHLaunch 
      
#'''
    
    message = rocket_name + " has an altitude of " + str(currentRocket.altitude) + " m. "
    if (currentRocket.stability > 0):
        message = message + user_request_rocket + " is stable at: " + str(currentRocket.stability)
    else:
        message = message + "Don't fly, the rocket is unstable" 

    resp = twilio.twiml.Response()
    resp.message(message)
 
    return str(resp)
 
if __name__ == "__main__":
    app.run(port=3000, host="0.0.0.0")

    

