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

from Game_engine import *

class ShooterApp(App):
	
	def build(self):
		global WIDTH
		global HEIGHT
		game = ShooterGame(WIDTH, HEIGHT)
		Clock.schedule_interval(game.game_update, 1.0 / 60.0)
		return game

if __name__ == '__main__':
	ShooterApp().run()