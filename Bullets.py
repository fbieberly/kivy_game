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

class PlayerBullet(Widget):
	name = 'pbullet'
	health = NumericProperty(5)
	velocity_x = NumericProperty(0)
	velocity_y = NumericProperty(6)
	velocity = ReferenceListProperty(velocity_x, velocity_y)

	def update(self):
		ret = True
		self.pos = Vector(*self.velocity) + self.pos

		if self.y > self.parent.top + 100 or self.y < -100 or self.x > self.parent.width+100 or self.x < -100:
			ret = False
		elif self.health <= 0:
			ret = False
		if ret == False:
			self.parent.remove_widget(self)
		return ret

class EnemyBullet(Widget):
	name = 'ebullet'
	health = NumericProperty(5)
	velocity_x = NumericProperty(0)
	velocity_y = NumericProperty(-4)
	velocity = ReferenceListProperty(velocity_x, velocity_y)

	def update(self):
		ret = True
		self.pos = Vector(*self.velocity) + self.pos

		if self.y > self.parent.top + 100 or self.y < -100 or self.x > self.parent.width+100 or self.x < -100:
			ret = False
		elif self.health <= 0:
			ret = False
		if ret == False:
			self.parent.remove_widget(self)
		return ret
