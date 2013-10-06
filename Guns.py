from sys import exit
from time import time
from random import randint, choice, random, uniform
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
	ObjectProperty
from kivy.vector import Vector
from kivy.core.audio import SoundLoader

from Bullets import *

class RepeaterGun(Widget):
	name = 'pgun'
	level = 1
	gun_cooldown = 0
	gun_fire_interval = 0.3
	bullet_strength = 70

	def __init__(self, **kwargs):
		super(RepeaterGun, self).__init__(**kwargs)
		self.gun_cooldown = time()
		self.laser = SoundLoader.load('laser.ogg')
		# self.laser.stop()
		# self.laser.loop = False

	def shoot(self):
		ret = True

		if self.parent.gun_level == 1:
			gun_fire_interval = 0.3
			bullet_speed = 6
			bullet_damage = 100
			bullet_angle = uniform(-0.3, 0.3)

			if time() > self.gun_cooldown:
				if self.laser:
					self.laser.play()
				bullet = PlayerBullet(	self.parent.center_x, 
										self.parent.top, bullet_speed, 
										bullet_angle, bullet_damage)
				self.parent.parent.add_widget(bullet)
				self.gun_cooldown = time() + gun_fire_interval
				self.parent.parent.score -= 1

		elif self.parent.gun_level == 2:
			gun_fire_interval = 0.15
			bullet_speed = 7
			bullet_damage = 100
			bullet_angle = uniform(-0.3, 0.3)

			if time() > self.gun_cooldown:
				if self.laser:
					self.laser.play()
				bullet = PlayerBullet(	self.parent.center_x, 
										self.parent.top, bullet_speed, 
										bullet_angle, bullet_damage)
				self.parent.parent.add_widget(bullet)
				self.gun_cooldown = time() + gun_fire_interval
				self.parent.parent.score -= 1

		return ret

class SpreadGun(Widget):
	name = 'pgun'
	gun_cooldown = 0

	def __init__(self, **kwargs):
		super(SpreadGun, self).__init__(**kwargs)
		self.gun_cooldown = time()
		self.laser = SoundLoader.load('laser.ogg')

	def shoot(self):
		ret = True

		if self.parent.gun_level == 1:
			gun_fire_interval = 0.4
			bullet_speed = 6
			bullet_damage = 100
			bullet_angle = -5

			if time() > self.gun_cooldown:
				if self.laser:
					self.laser.play()
				bullet = PlayerBullet(	self.parent.center_x, 
											self.parent.top, bullet_speed, 
											0, bullet_damage)
				self.parent.parent.add_widget(bullet)
				for xx in xrange(2):
					bullet = PlayerBullet(	self.parent.center_x, 
											self.parent.top, bullet_speed, 
											bullet_angle, bullet_damage)
					self.parent.parent.add_widget(bullet)
					bullet_angle += 10

				self.gun_cooldown = time() + gun_fire_interval
				self.parent.parent.score -= 1

		elif self.parent.gun_level == 2:
			gun_fire_interval = 0.35
			bullet_speed = 6
			bullet_damage = 100
			bullet_angle = -7.5

			if time() > self.gun_cooldown:
				if self.laser:
					self.laser.play()
				bullet = PlayerBullet(	self.parent.center_x, 
											self.parent.top, bullet_speed, 
											0, bullet_damage)
				self.parent.parent.add_widget(bullet)
				for xx in xrange(4):
					bullet = PlayerBullet(	self.parent.center_x, 
											self.parent.top, bullet_speed, 
											bullet_angle, bullet_damage)
					self.parent.parent.add_widget(bullet)
					bullet_angle += 5

				self.gun_cooldown = time() + gun_fire_interval
				self.parent.parent.score -= 1

		return ret