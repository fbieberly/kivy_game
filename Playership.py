from sys import exit
from time import time
from random import randint, choice, random, uniform
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
	ObjectProperty
from kivy.vector import Vector
from kivy.core.audio import SoundLoader

from Bullets import *
from Misc_objects import *
from Guns import *

class PlayerShip(Widget):
	name = 'player'
	health = 100
	gun_cooldown = time()
	gun_fire_interval = 0.1
	bullet_strength = 70
	gun_level = 2
	vel = 4
	velocity_x = NumericProperty(0)
	velocity_y = NumericProperty(0)
	velocity = ReferenceListProperty(velocity_x, velocity_y)

	keyboard_inputs = []
	_keyboard = None

	def __init__(self, x, y, **kwargs):
		super(PlayerShip, self).__init__(**kwargs)
		self.x = x
		self.y = y
		self.gun = RepeaterGun()
		self.add_widget(self.gun)
		self.boom = SoundLoader.load('boom.ogg')

	def _keyboard_closed(self):
		self._keyboard.unbind(on_key_down=self._on_keyboard_down)
		self._keyboard = None

	def _on_keyboard_down(self, keyboard, keycode, text, modifiers, *args):
		commands = ['a', 's', 'd', 'w', 'spacebar', 'escape']
		if keycode[1] in commands and keycode[1] not in self.keyboard_inputs:
			self.keyboard_inputs.append(keycode[1])
		# Return True to accept the key. Otherwise, it will be used by
		# the system.
		return True

	def _on_keyboard_up(self, keyboard, keycode, *args):
		commands = ['a', 's', 'd', 'w', 'spacebar', 'escape']
		if keycode[1] in commands:
			try:
				self.keyboard_inputs.remove(keycode[1])
			except:
				pass
		# Return True to accept the key. Otherwise, it will be used by
		# the system.
		return True

	def spawn_debris(self, x, y):
		dirs = [-2, -1, 0, 1, 2]
		for xx in range(15):
			tmp_debris = Debris(x, y)
			tmp_debris.velocity_x = choice(dirs)
			tmp_debris.velocity_y = choice(dirs)
			self.parent.add_widget(tmp_debris)

	def update(self):
		ret = True
		if self._keyboard == None:
			self._keyboard = Window.request_keyboard(
			self._keyboard_closed, self)
			self._keyboard.bind(on_key_down=self._on_keyboard_down)
			self._keyboard.bind(on_key_up=self._on_keyboard_up)

		self.velocity_x = 0
		self.velocity_y =0
		# print self.keyboard_inputs

		if self.health <= 0:
			if self.boom:
				self.boom.play()
			self.spawn_debris(self.x, self.y)
			self.parent.player_lives -= 1
			self.parent.player_dead = True
			self.parent.dead_time = time()
			self.parent.remove_widget(self)
		
		if 'a' in self.keyboard_inputs:
			self.velocity_x -= self.vel
		if 'd' in self.keyboard_inputs:
			self.velocity_x += self.vel
		if 'w' in self.keyboard_inputs:
			self.velocity_y += self.vel
		if 's' in self.keyboard_inputs:
			self.velocity_y -= self.vel

		if 'spacebar' in self.keyboard_inputs:
			self.gun.shoot()

		if 'escape' in self.keyboard_inputs:
				self.parent.game_state = 'pause_menu'

		self.pos = Vector(*self.velocity) + self.pos

		if self.x < 0:
			self.x = 0
		if self.x > self.parent.width - self.width:
			self.x = self.parent.width - self.width
		if self.y < 0:
			self.y = 0
		if self.y > self.parent.height - self.height:
			self.y = self.parent.height - self.height
		return ret

