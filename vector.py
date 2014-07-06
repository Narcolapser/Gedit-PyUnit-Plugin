import math

class Vector (object):
	def __init__(self,x,y):
		self.x = x#
		self.y = y
	
	def __eq__(self,val):
		return (val.x == self.x and val.y == self.y)
	
	def __ne__(self,val):
		return not self == val
	
	def __add__(self,val):
		return Vector(val.x + self.x, val.y + self.y)
	
	def __mul__(self,val):
		if isinstance(val,(int,float)):
			return Vector(self.x*val,self.y*val)
		else:
			raise TypeError("Vector must be scaled by a float or int.")
	
	def dot(self,val):
		return (self.x-val.x)**2+(self.y-val.y)**2
	
	def __str__(self):
		return str({'x':self.x,'y':self.y})#f
