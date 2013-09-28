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

from Bullets import *

class PlayerShip(Widget):
	name = 'player'
	health = NumericProperty(100)
	gun_cooldown = time()
	gun_fire_interval = 0.1
	bullet_strength = 70
	move_text = []
	velocity_x = NumericProperty(0)
	velocity_y = NumericProperty(0)
	velocity = ReferenceListProperty(velocity_x, velocity_y)

	def update(self):
		vel = 4
		self.velocity_x = 0
		self.velocity_y =0
		if 'a' in self.move_text:
			self.velocity_x -= vel
		if 'd' in self.move_text:
			self.velocity_x += vel
		if 'w' in self.move_text:
			self.velocity_y += vel
		if 's' in self.move_text:
			self.velocity_y -= vel
		self.pos = Vector(*self.velocity) + self.pos