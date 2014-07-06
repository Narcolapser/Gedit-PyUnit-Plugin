import unittest
import time
from vector import Vector

class TestVector (unittest.TestCase):

	def setUp(self):
		self.vec5 = Vector(5,5)
		self.vec1 = Vector(1,1)
		self.vec0 = Vector(0,0)
		self.vecu = Vector(4,0)
		self.veci = Vector(0,4)
	
	def test_eq(self):
		v5 = Vector(0,0)
		v5.x = 5
		v5.y = 5
		#self.assertEqual(v5,self.vec5)
		self.assertTrue(v5 == self.vec5)
		self.assertTrue((v5 == self.vec1) is False)
	
	def test_ne(self):
		v5 = Vector(0,0)
		v5.x = 5
		v5.y = 5
		self.assertEqual(v5,self.vec5)
		self.assertTrue(v5 != self.vec1)
		self.assertTrue((v5 != self.vec5) is False)
	
	def test_add(self):
		v4 = self.vecu + self.veci
		self.assertEqual(v4,Vector(4,4))
		self.assertEqual(v4+self.vec1,self.vec5)
	
	def test_scale(self):
		v5 = self.vec1*4
		self.assertEqual(v5,self.vec5)
		self.assertRaises(TypeError,v5.__mul__,self.vec5)
	
	def test_dot(self):
		self.assertEqual(self.vecu.dot(self.veci),32)
	
	def test_str(self):
		#time.sleep(10)
		self.assertEqual(str("{'y': 5, 'x': 5}"),str(self.vec5))


if __name__ == '__main__':
	unittest.main()


