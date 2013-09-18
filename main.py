from sys import exit
from time import time
from random import randint
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
	ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock

from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')

class PlayerBullet(Widget):
	name = 'bullet'
	health = NumericProperty(5)
	velocity_x = NumericProperty(0)
	velocity_y = NumericProperty(5)
	velocity = ReferenceListProperty(velocity_x, velocity_y)

	def update(self):
		self.pos = Vector(*self.velocity) + self.pos

class EnemyShip(Widget):
	name = 'enemy'
	health = NumericProperty(100)
	velocity_x = NumericProperty(0)
	velocity_y = NumericProperty(0)
	velocity = ReferenceListProperty(velocity_x, velocity_y)

	def update(self):
		self.pos = Vector(*self.velocity) + self.pos

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
		vel = 3
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

class ShooterGame(Widget):
	player1 = ObjectProperty(None)
	label1 = ObjectProperty(None)
	
	def __init__(self, **kwargs):
		super(ShooterGame, self).__init__(**kwargs)
		self._keyboard = Window.request_keyboard(
			self._keyboard_closed, self)
		self._keyboard.bind(on_key_down=self._on_keyboard_down)
		self._keyboard.bind(on_key_up=self._on_keyboard_up)

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
				self.player1.gun_cooldown = time() + self.player1.gun_fire_interval

		bullet_pos = []

		for child in self.children:
			child_name = None
			try:
				child_name = child.name
			except:
				pass
			if child_name == 'bullet': 
				child.update()
				bullet_pos.append((child.x + child.width/2, child.y + child.height/2))
				if child.y > self.height + 100:
					self.remove_widget(child)
				if child.health < 0:
					self.remove_widget(child)
			elif child_name == 'player':
				child.update()
			elif child_name == 'enemy':
				child.update()
				for point in bullet_pos:
					if child.collide_point(point[0], point[1]):
						child.health -= self.player1.bullet_strength
						for child2 in self.children:
							if  child2.x + child2.width/2 == point[0] and \
								child2.y + child2.height/2 == point[1] :
							   child2.health -= 10
							   break
				if child.health < 0:
					self.remove_widget(child)
					enemy = EnemyShip()
					enemy.x = randint(100, self.width - 100)
					enemy.y = randint(300, self.top - 30)
					self.add_widget(enemy)
		

		self.label1.text = str(self.player1.move_text)
		pass

class ShooterApp(App):
	def build(self):
		game = ShooterGame()
		Clock.schedule_interval(game.update, 1.0 / 60.0)
		return game

if __name__ == '__main__':
	ShooterApp().run()