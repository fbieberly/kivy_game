from sys import exit
from time import time
from random import randint, choice, random
from kivy.app import App
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.core.window import Window, Keyboard
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
	keyboard_inputs = []
	game_state = 'start_menu'

	# keyboard keys
	a = 97
	s = 115
	d = 100
	w = 119
	space = 32
	escape = 27
	
	def __init__(self, width, height, **kwargs):
		super(ShooterGame, self).__init__(**kwargs)
		self.width = width
		self.height = height

	def game_update(self, dt):
		ret = True
		bullet_pos = []
		pbullets = []
		ebullets = []
		enemies = []
		players = []

		if self.game_state == 'start_menu':
			start_menu = StartMenu()
			start_menu.width = self.width
			start_menu.height = self.height
			self.add_widget(start_menu)
			ret = False
		elif self.game_state == 'pause_menu':
			pause_menu = PauseMenu()
			pause_menu.width = self.width
			pause_menu.height = self.height
			self.add_widget(pause_menu)
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

			for bullet in pbullets:
				for enemy in enemies:
					bullet.check_collision(enemy)

			for bullet in ebullets:
				for player in players:
					bullet.check_collision(player)
		return ret