"""
						== Vector ==
Description:	A simple library for easy use of vectors.
Author: 		Arnaud Levaufre


						== MANUAL ==
class :
-------

Vector : Vector object wich provide some method for
	rapid calculation of basic vector property such as
	norm and unitary vector.
	Vector2 and Vector3 may be used instead of the general
	Vector class, so you will have acces to x,y,z coordinates
	as properties.
	
	class methods:
	--------------
	getNorm :: self:Vector -> float
		return the norm of the vector.
	getunitary :: self:Vector -> Vector
		return the unitary vector.


Functions :
-----------

scalarProduct :: vect1:Vector, vect2:Vector -> float
	Calculate the scalar product of vect1 and vect2

crossProduct :: vect1:Vector3, vect2:Vector3 -> Vector3
	Calculate the vectorial product of vect1 by vect2


"""

import math

# -------------------~=====~------------------- #
# -                   CLASS                   - #

class Vector(object):
	def __init__(self, *args):
		self.coords = []
		for arg in args:
			self.coords.append(arg)
	
	def set(self, *args):
		if len(args) == len(self.coords):
			for i in xrange(len(args)):
				self.coords[i] = args[i]
	
	def getNorm(self):
		"""
		Calculate the norm of the vector
		"""

		coordSum = 0
		for coord in self.coords:
			coordSum += coord**2
		return math.sqrt(coordSum)

	def getUnitary(self):
		"""
		Calculate the unitary vector.
		"""

		norm = self.getNorm()
		unitaryCoord = [ coord/norm for coord in self.coords ]
		
		# return a Vector or Vector2 or Vector3.
		if len(self.coords) == 2:
			return Vector2(*unitaryCoord)
		elif len(self.coords) == 3:
			return Vector3(*unitaryCoord)
		else:
			return Vector(*unitaryCoord)
	
class Vector2(Vector):
	def __init__(self, x,y):
		super(Vector2, self).__init__(x,y)
		self.x = self.coords[0]
		self.y = self.coords[1]

class Vector3(Vector):
	def __init__(self, x, y, z):
		super(Vector3, self).__init__(x,y,z)
		self.x = self.coords[0]
		self.y = self.coords[1]
		self.z = self.coords[2]



# -----------------~=========~----------------- #
# -                 FUNCTIONS                 - #

def scalarProduct(vect1, vect2):
	if len(vect1.coords) == len(vect2.coords):
		scalar = 0
		for i in xrange( len(vect1.coords) ):
			scalar += vect1.coords[i] * vect2.coords[i]
		return scalar
	else:
		return None

def crossProduct(vect1, vect2):
	if 2 <= len(vect1.coords) <= 3 and 2 <= len(vect2.coords) <= 3:
		if len(vect1.coords) == 2:
			vect1 = Vector3(vect1.coords[0], vect1.coords[1], 0)
		if len(vect2.coords) == 2:
			vect2 = Vector3(vect2.coords[0], vect2.coords[1], 0)
		
		x = vect1.coords[1]*vect2.coords[2] - vect1.coords[2]*vect2.coords[1]
		y = vect1.coords[2]*vect2.coords[0] - vect1.coords[0]*vect2.coords[2]
		z = vect1.coords[0]*vect2.coords[1] - vect1.coords[1]*vect2.coords[0]
		
		return Vector3(x,y,z)
	else:
		return None

# -------------------~=====~------------------- #
# -                   ALIAS                   - #

vectorProduct 	= crossProduct
dotProduct 		= scalarProduct


if __name__ == "__main__":

	vector31 = Vector(2,2,2)
	vector32 = Vector(4,5,4)
	
	print crossProduct(vector31, vector32).coords, vectorProduct(vector31, vector32).coords
