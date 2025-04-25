from model import Model
from controller import Controller
from view import View



m = Model()
v = View()
c = Controller(m, v)

c.run()