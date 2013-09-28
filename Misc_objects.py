from sys import exit
from time import time
from random import randint, choice, random
from kivy.app import App
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
	ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock

class Debris(Widget):
	name = 'debris'
	color1 = 1.0
	color2 = 0.5
	health = 10
	size1 = 10
	size_decrease = random()
	health = NumericProperty(10)
	velocity_x = NumericProperty(0)
	velocity_y = NumericProperty(0)
	velocity = ReferenceListProperty(velocity_x, velocity_y)

	def __init__(self, **kwargs):
		super(Debris, self).__init__(**kwargs)
		self.size_decrease = random()

	def update(self):
		ret = True
		self.canvas.clear()
		self.canvas.add(Color(self.color1, self.color2, 0))
		self.canvas.add(Rectangle(pos=self.pos,size=(int(self.size1),int(self.size1))))
		self.color1 -= 0.02
		self.color2 -= 0.02
		self.size1 -= self.size_decrease*0.1
		self.pos = Vector(*self.velocity) + self.pos
		if self.color2 <= 0:
			ret = False
		if self.y > self.parent.top + 100 or self.y < -100 or self.x > self.parent.width+100 or self.x < -100:
			ret = False
		elif self.health <= 0:
			ret = False
		if ret == False:
			self.parent.remove_widget(self)
		return ret
