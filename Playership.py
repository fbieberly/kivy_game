from sys import exit
from time import time
from random import randint, choice, random
from kivy.app import App
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
	ObjectProperty
from kivy.vector import Vector

from Bullets import *

class PlayerShip(Widget):
	name = 'player'
	health = NumericProperty(100)
	gun_cooldown = time()
	gun_fire_interval = 0.1
	bullet_strength = 70
	vel = 4
	velocity_x = NumericProperty(0)
	velocity_y = NumericProperty(0)
	velocity = ReferenceListProperty(velocity_x, velocity_y)

	def __init__(self, x, y, **kwargs):
		super(PlayerShip, self).__init__(**kwargs)
		self.x = x
		self.y = y

	def check_keyboard_inputs(self, inputs):
		self.velocity_x = 0
		self.velocity_y =0
		if 'a' in inputs:
			self.velocity_x -= self.vel
		if 'd' in inputs:
			self.velocity_x += self.vel
		if 'w' in inputs:
			self.velocity_y += self.vel
		if 's' in inputs:
			self.velocity_y -= self.vel

		if 'spacebar' in inputs:
			if time() > self.gun_cooldown:
				bullet = PlayerBullet(self.center_x, self.top, 100, 0, 100)
				self.parent.add_widget(bullet)
				self.gun_cooldown = time() + self.gun_fire_interval

	def update(self):

		self.pos = Vector(*self.velocity) + self.pos

		if self.x < 0:
			self.x = 0
		if self.x > self.parent.width - self.width:
			self.x = self.parent.width - self.width
		if self.y < 0:
			self.y = 0
		if self.y > self.parent.height - self.height:
			self.y = self.parent.height - self.height