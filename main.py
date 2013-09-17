from sys import exit
from time import time
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
	health = NumericProperty(0)
	velocity_x = NumericProperty(0)
	velocity_y = NumericProperty(5)
	velocity = ReferenceListProperty(velocity_x, velocity_y)

	def update(self):
		self.pos = Vector(*self.velocity) + self.pos


class PlayerShip(Widget):
	name = 'player'
	health = NumericProperty(0)
	gun_cooldown = time()
	gun_fire_interval = 0.1
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
	bullets = []
	
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
		#self.player1.update()

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
				bullet.x = self.player1.x
				bullet.y = self.player1.y
				#self.bullets.append(bullet)
				self.add_widget(bullet)
				self.player1.gun_cooldown = time() + self.player1.gun_fire_interval
			# bullet.x = self.player1.x
			# bullet.y = self.player1.y

		for child in self.children:
			try: 
				child.update()
				if child.y > self.height:
					self.remove_widget(child)
			except:
				pass
		

		self.label1.text = str(self.player1.move_text)
		pass

class ShooterApp(App):
	def build(self):
		game = ShooterGame()
		Clock.schedule_interval(game.update, 1.0 / 60.0)
		return game

if __name__ == '__main__':
	ShooterApp().run()