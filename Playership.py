from sys import exit
from time import time
from random import randint, choice, random
from kivy.app import App
from kivy.core.window import Window
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

	keyboard_inputs = []
	# keyboard keys
	a = 97
	s = 115
	d = 100
	w = 119
	space = 32
	escape = 27

	def __init__(self, x, y, **kwargs):
		super(PlayerShip, self).__init__(**kwargs)
		self.x = x
		self.y = y

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

	def update(self):
		if self._keyboard == None:
			self._keyboard = Window.request_keyboard(
			self._keyboard_closed, self)
			self._keyboard.bind(on_key_down=self._on_keyboard_down)
			self._keyboard.bind(on_key_up=self._on_keyboard_up)

		self.velocity_x = 0
		self.velocity_y =0
		if 'a' in self.keyboard_inputs:
			self.velocity_x -= self.vel
		if 'd' in self.keyboard_inputs:
			self.velocity_x += self.vel
		if 'w' in self.keyboard_inputs:
			self.velocity_y += self.vel
		if 's' in self.keyboard_inputs:
			self.velocity_y -= self.vel

		if 'spacebar' in self.keyboard_inputs:
			if time() > self.gun_cooldown:
				bullet = PlayerBullet(self.center_x, self.top, 100, 0, 100)
				self.parent.add_widget(bullet)
				self.gun_cooldown = time() + self.gun_fire_interval

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