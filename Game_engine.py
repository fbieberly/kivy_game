from sys import exit
from time import time
from random import randint, choice, random
from kivy.app import App
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, ReferenceListProperty,\
	ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock

from Menus import *
from Enemies import *
from Playership import *
from Misc_objects import *


class ShooterGame(Widget):
	pbullets = []
	ebullets = []
	enemies = []
	debris = []
	keyboard_commands = []
	game_state = 'start_menu'

	
	def __init__(self, width, height, **kwargs):
		super(ShooterGame, self).__init__(**kwargs)
		self._keyboard = Window.request_keyboard(
			self._keyboard_closed, self)
		self._keyboard.bind(on_key_down=self._on_keyboard_down)
		self._keyboard.bind(on_key_up=self._on_keyboard_up)
		self.width = width
		self.height = height

		# player1 = PlayerShip(width/2, 30)
		# self.add_widget(player1)

		# enemy = EnemyShip(randint(200, width-200), randint(height - 300, height - 30))
		# enemy.velocity_y = randint(-2,-1)
		# enemy.velocity_x = randint(-2, 2)
		# self.add_widget(enemy)

	def _keyboard_closed(self):
		self._keyboard.unbind(on_key_down=self._on_keyboard_down)
		self._keyboard = None

	def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
		#self.label1.text = keycode[1]
		commands = ['a', 's', 'd', 'w', 'spacebar', 'escape']
		if keycode[1] in commands and keycode[1] not in self.keyboard_commands:
			self.keyboard_commands.append(keycode[1])

		# Return True to accept the key. Otherwise, it will be used by
		# the system.
		return True

	def _on_keyboard_up(self, keyboard, keycode):
		#self.label1.text = keycode[1]
		commands = ['a', 's', 'd', 'w', 'spacebar', 'escape']
		if keycode[1] in commands:
			try:
				self.keyboard_commands.remove(keycode[1])
			except:
				pass

		# if keycode[1] == 'escape':
		# 	exit(0)

		# Return True to accept the key. Otherwise, it will be used by
		# the system.
		return True

	def game_update(self, dt):
		ret = True
		bullet_pos = []
		pbullets = []
		ebullets = []
		enemies = []
		players = []

		if self.game_state == 'start_menu':
			# print self.game_state, time()
			# self.game_state = 'playing'
			start_menu = StartMenu()
			start_menu.width = self.width
			start_menu.height = self.height
			self.add_widget(start_menu)
			ret = False
		elif self.game_state == 'loading':
			self.game_state = 'playing'
			player1 = PlayerShip(self.width/2, 30)
			self.add_widget(player1)

			enemy = EnemyShip(randint(200, self.width-200), randint(self.height - 300, self.height - 30))
			enemy.velocity_y = randint(-2,-1)
			enemy.velocity_x = randint(-2, 2)
			self.add_widget(enemy)
		elif self.game_state == 'playing':

			for child in self.children:
				child_name = None
				try:
					child_name = child.name
					child.update()
				except:
					pass
				if child_name == 'pbullet':
					pbullets.append(child)
				elif child_name == 'ebullet':
					ebullets.append(child)
				elif child_name == 'enemy':
					enemies.append(child)
				elif child_name == 'player':
					players.append(child)

			for player in players:
				player.check_keyboard_inputs(self.keyboard_commands)

			for bullet in pbullets:
				for enemy in enemies:
					bullet.check_collision(enemy)

			for bullet in ebullets:
				for player in players:
					bullet.check_collision(player)

		if 'escape' in self.keyboard_commands:
			pause_menu = PauseMenu()
			pause_menu.width = self.width
			pause_menu.height = self.height
			self.add_widget(pause_menu)
			ret = False
		return ret