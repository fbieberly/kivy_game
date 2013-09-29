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

# from Game_engine import *

class StartMenu(Widget):
	but1 = ObjectProperty(None)
	but2 = ObjectProperty(None)
	but3 = ObjectProperty(None)

	keyboard_inputs = []

	def __init__(self, **kwargs):
		super(StartMenu, self).__init__(**kwargs)
		Clock.schedule_interval(self.update, 1.0 / 30.0)

	def update(self, dt):
		x, y = Window.mouse_pos
		buttons = [self.but1, self.but2, self.but3]
		# self.but1.font_size = 100
		for button in buttons:
			if button.collide_point(x, y):
				button.font_size = 70
				button.color = (1, .8, .1, 1)
			else:
				button.font_size = 50
				button.color = (1, 1, 1, 1)
		return True

	def start_game(self):
		self.parent.game_state = 'loading'
		Clock.schedule_interval(self.parent.game_update, 1.0 / 60.0)
		self.parent.remove_widget(self)
		
	def quit(self):
		exit(0)

class PauseMenu(Widget):
	but1 = ObjectProperty(None)
	but2 = ObjectProperty(None)
	but3 = ObjectProperty(None)
	keyboard_inputs = []

	def __init__(self, **kwargs):
		super(PauseMenu, self).__init__(**kwargs)
		Clock.schedule_interval(self.update, 1.0 / 30.0)
		self._keyboard = Window.request_keyboard(
			self._keyboard_closed, self)
		self._keyboard.bind(on_key_down=self._on_keyboard_down)
		self._keyboard.bind(on_key_up=self._on_keyboard_up)

	def _keyboard_closed(self):
		self._keyboard.unbind(on_key_down=self._on_keyboard_down)
		self._keyboard = None
		# Window.unbind(on_key_down=self._on_keyboard_down)

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

	def update(self, dt):
		x, y = Window.mouse_pos
		buttons = [self.but1, self.but2, self.but3]

		if 'escape' in self.keyboard_inputs:
			self.parent.game_state = 'playing'
			Clock.schedule_interval(self.parent.game_update, 1.0 / 60.0)
			self.parent.remove_widget(self)

		for button in buttons:
			if button.collide_point(x, y):
				button.font_size = 70
				button.color = (1, .8, .1, 1)
			else:
				button.font_size = 50
				button.color = (1, 1, 1, 1)
		return True



	def resume_game(self):
		self.parent.game_state = 'playing'
		Clock.schedule_interval(self.parent.game_update, 1.0 / 60.0)
		self.parent.remove_widget(self)
		
	def quit(self):
		exit(0)