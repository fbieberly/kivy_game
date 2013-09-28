from kivy.config import Config
WIDTH = 800
HEIGHT = 600
Config.set('graphics', 'width', WIDTH)
Config.set('graphics', 'height', HEIGHT)
Config.write()

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

from Enemies import *
from Playership import *
from Misc_objects import *

class ShooterGame(Widget):
	player1 = None
	pbullets = []
	ebullets = []
	enemies = []
	debris = []
	keyboard_commands = []
	
	def __init__(self, **kwargs):
		super(ShooterGame, self).__init__(**kwargs)
		self._keyboard = Window.request_keyboard(
			self._keyboard_closed, self)
		self._keyboard.bind(on_key_down=self._on_keyboard_down)
		self._keyboard.bind(on_key_up=self._on_keyboard_up)

		self.player1 = PlayerShip(WIDTH/2, 30)
		self.add_widget(self.player1)

		enemy = EnemyShip(randint(200, WIDTH-200), randint(HEIGHT - 300, HEIGHT - 30))
		enemy.velocity_y = randint(-2,-1)
		enemy.velocity_x = randint(-2, 2)
		self.add_widget(enemy)

	def _keyboard_closed(self):
		self._keyboard.unbind(on_key_down=self._on_keyboard_down)
		self._keyboard = None

	def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
		#self.label1.text = keycode[1]
		commands = ['a', 's', 'd', 'w', 'spacebar']
		if keycode[1] in commands and keycode[1] not in self.keyboard_commands:
			self.keyboard_commands.append(keycode[1])

		# Return True to accept the key. Otherwise, it will be used by
		# the system.
		return True

	def spawn_debris(self, x, y):
		dirs = [-2, -1, 1, 2]
		for xx in range(10):
			tmp_debris = Debris(x, y)
			tmp_debris.velocity_x = choice(dirs)
			tmp_debris.velocity_y = choice(dirs)
			self.add_widget(tmp_debris)

	def _on_keyboard_up(self, keyboard, keycode):
		#self.label1.text = keycode[1]
		commands = ['a', 's', 'd', 'w', 'spacebar']
		if keycode[1] in commands:
			try:
				self.keyboard_commands.remove(keycode[1])
			except:
				pass

		if keycode[1] == 'escape':
			exit(0)

		# Return True to accept the key. Otherwise, it will be used by
		# the system.
		return True

	def update(self, dt):



		bullet_pos = []
		pbullets = []
		ebullets = []
		enemies = []
		players = []

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

		return True

class ShooterApp(App):
	def build(self):
		game = ShooterGame()
		Clock.schedule_interval(game.update, 1.0 / 60.0)
		return game

if __name__ == '__main__':

	ShooterApp().run()