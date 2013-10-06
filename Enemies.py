from sys import exit
from time import time
from random import randint, choice, random, uniform
from kivy.app import App
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
	ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

from Bullets import *
from Misc_objects import *

class EnemyShip(Widget):
	name = 'enemy'
	min_y = NumericProperty(200)
	health = NumericProperty(100)
	velocity_x = NumericProperty(0)
	velocity_y = NumericProperty(0)
	gun_cooldown = time()
	gun_fire_interval = 1.2

	velocity = ReferenceListProperty(velocity_x, velocity_y)

	def __init__(self, x, y, **kwargs):
		super(EnemyShip, self).__init__(**kwargs)
		self.x = x
		self.y = y
		self.boom = SoundLoader.load('boom.ogg')

	def spawn_debris(self, x, y):
		dirs = [-2, -1, 0, 1, 2]
		for xx in range(10):
			tmp_debris = Debris(x, y)
			tmp_debris.velocity_x = choice(dirs)
			tmp_debris.velocity_y = choice(dirs)
			self.parent.add_widget(tmp_debris)

	def check_collision(self, target):
		if target.collide_widget(self):
			target.health -= self.health
			self.health = 0

	def update(self):
		ret = True
		self.pos = Vector(*self.velocity) + self.pos
		if time() > self.gun_cooldown:
			bullet = EnemyBullet()
			bullet.x = self.x + self.width/2
			bullet.y = self.y
			self.parent.add_widget(bullet)
			self.gun_cooldown = time() + self.gun_fire_interval


		if self.y < self.min_y and self.velocity_y < 0:
			self.velocity_y *= -1
		if self.y > self.parent.top + 100 or self.y < -100 or self.x > self.parent.width+100 or self.x < -100:
			ret = False
		elif self.health <= 0:
			self.spawn_debris(self.x, self.y)
			if self.boom:
				self.boom.play()
			ret = False
		if ret == False:
			enemy = EnemyShip(randint(0, self.parent.width), 
				self.parent.height + 50)
			enemy.velocity_y = uniform(-2,-1)
			enemy.velocity_x = uniform(-2, 2)
			self.parent.add_widget(enemy)
			self.parent.remove_widget(self)
		return ret

