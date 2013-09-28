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

class EnemyShip(Widget):
	name = 'enemy'
	min_y = NumericProperty(200)
	health = NumericProperty(100)
	velocity_x = NumericProperty(0)
	velocity_y = NumericProperty(0)
	gun_cooldown = time()
	gun_fire_interval = 1.2

	velocity = ReferenceListProperty(velocity_x, velocity_y)

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
			self.parent.spawn_debris(self.x, self.y)
			ret = False
		if ret == False:
			enemy = EnemyShip()
			enemy.x = randint(100, self.parent.width - 100)
			enemy.y = randint(300, self.parent.top - 30)
			enemy.velocity_y = randint(-2,-1)
			enemy.velocity_x = randint(-2, 2)
			self.parent.add_widget(enemy)
			self.parent.remove_widget(self)
		return ret

