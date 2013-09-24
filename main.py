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

from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')

class PlayerBullet(Widget):
	name = 'pbullet'
	health = NumericProperty(5)
	velocity_x = NumericProperty(0)
	velocity_y = NumericProperty(6)
	velocity = ReferenceListProperty(velocity_x, velocity_y)

	def update(self):
		ret = True
		self.pos = Vector(*self.velocity) + self.pos

		if self.y > self.parent.top + 100 or self.y < -100 or self.x > self.parent.width+100 or self.x < -100:
			ret = False
		elif self.health <= 0:
			ret = False
		if ret == False:
			self.parent.remove_widget(self)
		return ret

class EnemyBullet(Widget):
	name = 'ebullet'
	health = NumericProperty(5)
	velocity_x = NumericProperty(0)
	velocity_y = NumericProperty(-4)
	velocity = ReferenceListProperty(velocity_x, velocity_y)

	def update(self):
		ret = True
		self.pos = Vector(*self.velocity) + self.pos

		if self.y > self.parent.top + 100 or self.y < -100 or self.x > self.parent.width+100 or self.x < -100:
			ret = False
		elif self.health <= 0:
			ret = False
		if ret == False:
			self.parent.remove_widget(self)
		return ret

class Debris(Widget):
	name = 'debris'
	color1 = 1.0
	color2 = 0.5
	health = 10
	size1 = 10
	size_decrease = random()
	health = NumericProperty(10)
	velocity_x = NumericProperty(0)
	velocity_y = NumericProperty(0)
	velocity = ReferenceListProperty(velocity_x, velocity_y)

	def update(self):
		ret = True
		self.canvas.clear()
		self.canvas.add(Color(self.color1, self.color2, 0))
		self.canvas.add(Rectangle(pos=self.pos,size=(int(self.size1),int(self.size1))))
		self.color1 -= 0.02
		self.color2 -= 0.02
		self.size1 -= self.size_decrease
		self.pos = Vector(*self.velocity) + self.pos
		if self.color2 <= 0:
			ret = False
		if self.y > self.parent.top + 100 or self.y < -100 or self.x > self.parent.width+100 or self.x < -100:
			ret = False
		elif self.health <= 0:
			ret = False
		if ret == False:
			self.parent.remove_widget(self)
		return ret
			


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
		vel = 4
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
	pbullets = []
	ebullets = []
	enemies = []
	debris = []
	just_started = True

	
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

		if self.just_started:
			enemy = EnemyShip()
			enemy.x = randint(100, self.width - 100)
			enemy.y = randint(300, self.top - 30)
			enemy.velocity_y = randint(-2,-1)
			enemy.velocity_x = randint(-2, 2)
			self.add_widget(enemy)
			self.just_started = False

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
		
		self.label1.text = str(self.player1.move_text)
		pass

class ShooterApp(App):
	def build(self):
		game = ShooterGame()
		Clock.schedule_interval(game.update, 1.0 / 60.0)
		return game

if __name__ == '__main__':
	ShooterApp().run()