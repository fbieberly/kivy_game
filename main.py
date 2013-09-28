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
	
	def __init__(self, **kwargs):
		super(ShooterGame, self).__init__(**kwargs)
		self._keyboard = Window.request_keyboard(
			self._keyboard_closed, self)
		self._keyboard.bind(on_key_down=self._on_keyboard_down)
		self._keyboard.bind(on_key_up=self._on_keyboard_up)

		player1 = PlayerShip()
		player1.center_x = self.width / 2
		player1.center_y = 30
		self.add_widget(player1)
		self.player1 = player1

		enemy = EnemyShip()
		enemy.x = randint(200, WIDTH-200)
		enemy.y = randint(HEIGHT - 300, HEIGHT - 30)
		enemy.velocity_y = randint(-2,-1)
		enemy.velocity_x = randint(-2, 2)
		self.add_widget(enemy)

	def _keyboard_closed(self):
		self._keyboard.unbind(on_key_down=self._on_keyboard_down)
		self._keyboard = None

	def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
		#self.label1.text = keycode[1]
		commands = ['a', 's', 'd', 'w', 'spacebar']
		if keycode[1] in commands and keycode[1] not in self.player1.move_text:
			self.player1.move_text.append(keycode[1])

		# Return True to accept the key. Otherwise, it will be used by
		# the system.
		return True

	def spawn_debris(self, x, y):
		dirs = [-2, -1, 1, 2]
		for xx in range(10):
			tmp_debris = Debris()
			tmp_debris.x = x
			tmp_debris.y = y
			tmp_debris.velocity_x = choice(dirs)
			tmp_debris.velocity_y = choice(dirs)
			self.add_widget(tmp_debris)
			self.debris.append(tmp_debris)

	def _on_keyboard_up(self, keyboard, keycode):
		#self.label1.text = keycode[1]
		commands = ['a', 's', 'd', 'w', 'spacebar']
		if keycode[1] in commands:
			try:
				self.player1.move_text.remove(keycode[1])
			except:
				pass

		if keycode[1] == 'escape':
			exit(0)

		# Return True to accept the key. Otherwise, it will be used by
		# the system.
		return True

	def update(self, dt):
		if self.player1.x < self.x:
			self.player1.x = 0
		if self.player1.x > self.width - self.player1.width:
			self.player1.x = self.width - self.player1.width
		if self.player1.y < self.y:
			self.player1.y = 0
		if self.player1.y > self.height - self.player1.height:
			self.player1.y = self.height - self.player1.height

		if 'spacebar' in self.player1.move_text:
			if time() > self.player1.gun_cooldown:
				bullet = PlayerBullet()
				bullet.x = self.player1.x + self.player1.width/2
				bullet.y = self.player1.top
				self.add_widget(bullet)
				self.pbullets.append(bullet)
				self.player1.gun_cooldown = time() + self.player1.gun_fire_interval

		# for bullet in pbullets:
		# 	for ships in enemies:

		# 	if bullet.update() == False:
		# 		self.remove_widget(bullet)
		# 		pbullets.remove(bullet)

		bullet_pos = []
		pbullets = []
		ebullets = []

		for child in self.children:
			child_name = None
			try:
				child_name = child.name
			except:
				pass
			if child_name == 'pbullet':
				pbullets.append(child)
			if child_name == 'ebullet':
				ebullets.append(child)

		#print pbullets

		for child in pbullets:
			child.update()
			bullet_pos.append((child.x + child.width/2, child.y + child.height/2))
			if child.y > self.height + 100:
				self.remove_widget(child)
			if child.health < 0:
				self.remove_widget(child)

		for child in self.children:
			child_name = None
			try:
				child_name = child.name
			except:
				pass
			# if child_name == 'bullet': 
			# 	child.update()
			# 	bullet_pos.append((child.x + child.width/2, child.y + child.height/2))
			# 	if child.y > self.height + 100:
			# 		self.remove_widget(child)
			# 	if child.health < 0:
			# 		self.remove_widget(child)
			if child_name == 'player':
				child.update()
			elif child_name == 'debris':
				child.update()
			elif child_name == 'ebullet':
				child.update()
			elif child_name == 'enemy':
				child.update()
				for point in bullet_pos:
					if child.collide_point(point[0], point[1]):
						child.health -= self.player1.bullet_strength
						for child2 in self.children:
							if  child2.x + child2.width/2 == point[0] and child2.y + child2.height/2 == point[1] :
							   child2.health -= 10
							   break
		
		return True

class ShooterApp(App):
	def build(self):
		game = ShooterGame()
		Clock.schedule_interval(game.update, 1.0 / 60.0)
		return game

if __name__ == '__main__':

	ShooterApp().run()