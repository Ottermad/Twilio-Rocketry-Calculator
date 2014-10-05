# Import Statements
import math
import decimal

# Variables
LN	= 2.0	# length of nose
d	= 3.0	# diameter at base of nose
dF	= 4.0	# diameter at front of transition
dR	= 5.0	# diameter at rear of transition
LT	= 6.0	# length of transition
XP	= 7.0	# distance from tip of nose to front of transition
CR	= 8.0	# fin root chord
CT	= 9.0	# fin tip chord
S	= 1.0	# fin semispan
LF	= 2.0	# length of fin mid-chord line
R	= 3.0	# radius of body at aft end
XR	= 4.0	# distance between fin root leading edge and fin tip leading edge parallel to body
XB	= 5.0	# distance from nose tip to fin root chord leading edge
N	= 6.0	# number of fins

cnn = 2;
xn = 0;


class noseConeTypes:
	def __init__(self):
		self.cone = 1
		self.Ogive = 2

NoseConeTypes = noseConeTypes()


def cp(rocket):
	
	LN	= rocket.LN		# length of nose
	d	= rocket.d		# diameter at base of nose
	dF	= rocket.dF		# diameter at front of transition
	dR	= rocket.dR		# diameter at rear of transition
	LT	= rocket.LT		# length of transition
	XP	= rocket.XP		# distance from tip of nose to front of transition
	CR	= rocket.CR		# fin root chord
	CT	= rocket.CT		# fin tip chord
	S	= rocket.S		# fin semispan
	LF	= rocket.LF		# length of fin mid-chord line
	R	= rocket.R		# radius of body at aft end
	XR	= rocket.XR		# distance between fin root leading edge and fin tip leading edge parallel to body
	XB	= rocket.XB		# distance from nose tip to fin root chord leading edge
	N	= rocket.N		# number of fins

	if rocket.NCType == NoseConeTypes.cone:
		XN = 0.666 * N
	elif rocket.NCType == NoseConeTypes.Ogive:
		XN = 0.466 * N 
	else :
		print("Error, Cone was not recognised")	

	#cofp
	cnt = 2*( ((dR/d)**2) - ((dF) **2))
	xt = XP + (LT / 3) * (
		1 + ( 
				(1 - (dF / dR)) /
				(1 - ((dF / dR)**2)) 
			)
	)


	#XF

	Xf = XB + ((XR / 3.0) * ((CR+(2.0*CT)) / (CR+CT) ) + (1.0/6.0) * (
		(CR+CT) - ((CR*CT) / (CR+CT))
		)


		)

	#print Xf

	#cnf 
	raizcuadrada = math.sqrt(1 + ((2 * LF) / (CR + CT))**2)

	cnf =  (1.0 + (R/(S + R) ) ) * (

		((4.0 * N) * (S/d)*(S/d)) /

		(1.0 + raizcuadrada))

	#print cnf

	# Conical Transitions
	cnt = 2*( ((dR/d)**2) - ((dF) **2))
	xt = XP + (LT / 3) * (
		1 + ( 
				(1 - (dF / dR)) /
				(1 - ((dF / dR)**2)) 
			)
	)

	cnr = cnn + cnt + cnf
	x = (cnn * xn + cnt * xt + cnf * Xf )/ cnr
	return x

# TODO: Main Stuff
# Altitude
def altitude(M, dia, I, T):
	context = decimal.Context(prec=5, rounding=decimal.ROUND_DOWN)
	# Mass of rocket in kg
	M = decimal.Decimal(0.05398)
	dia = 0.976
	pi = context.create_decimal_from_float(math.pi)
	A = decimal.Decimal(pi * (decimal.Decimal(0.5 * (dia/12)*0.3048)**2) ) # TODO: Calculate area  
	Cd = decimal.Decimal(0.75)
	rho = decimal.Decimal(1.2)
	k = decimal.Decimal(decimal.Decimal(0.5) * rho*Cd*A)
	g = decimal.Decimal(9.8)
		
	I = decimal.Decimal(9)
	T = decimal.Decimal(6)
	t = I / T
	q = ((T - M*g) / k).sqrt()
	x = 2*k*q / M
	v_1 = 1-((-x*t).exp())
	v_2 = 1+((-x*t).exp())
	v = q*(v_1 / v_2)
	var = ((T - M*g - k*v**2) / (T - M*g))
	var2 = ((T - M*g - k*v**2) / (T - M*g)).ln()
	yb = decimal.Decimal((-M / (2*k)))* var2
	yc = (+M / (2*k))*(((M*g + k*v**2) / (M*g)).ln())
	altitude = yb + yc
	return altitude


class Component:
	def __init__(self, Mass, Distance):
		self.mass = Mass
		self.weight = self.mass * 9.8 #9.8 is the gravity
		self.distance = Distance

	def cgValue(self):
		return self.distance * self.weight

def getCentreOfGravity(Rocket):
	#Combine weights
	weight = Rocket.nose.weight;
	weight += Rocket.recovery.weight 
	weight += Rocket.body.weight 
	weight += Rocket.engine.weight 
	weight += Rocket.fins.weight
	#Work out the centre of gravity
	cg = (Rocket.nose.cgValue() + Rocket.recovery.cgValue() + Rocket.body.cgValue() + Rocket.engine.cgValue() + Rocket.fins.cgValue()) / weight
	return cg

class rocket:
    def __init__(self, Nose, NCType, Recovery, Body, Engine, Fins,
    			LN,d,dF,dR,LT,XP,CR,CT,S,LF,R,XR,XB,N):
    	#Centre of gravity
    	self.NCType = NCType
        self.nose = Nose
        self.recovery = Recovery
        self.body = Body
        self.engine = Engine 
        self.fins = Fins
        self.cg = getCentreOfGravity(self)
        #Rest of the code
        self.LN = LN
        self.d = d
        self.dF = dF
        self.dR = dR
        self.LT = LT
        self.XP = XP
        self.CR = CR
        self.CT = CT
        self.S = S
        self.LF = LF
        self.R = R
        self.D = R * 2
        self.XR = XR
        self.XB = XB
        self.N = N
        self.cp = cp(self)
        #Mass and weight
        self.mass = self.nose.mass + self.recovery.mass + self.body.mass + self.engine.mass + self.fins.mass
        self.weight = self.mass * 9.8
        self.altitude = altitude(self.mass, self.D,self.engine.impulse,self.engine.thrust) 
        self.stability = (self.cg - self.cp) - self.D


class Motor:
	def __init__(self,impulse,thrust,mass,distance):
		self.impulse = impulse
		self.thrust = thrust
		self.mass = mass
		self.weight = mass * 9.8
		self.distance = distance
	def cgValue(self):
		return self.distance * self.weight



