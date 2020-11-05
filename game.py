
import discord
from random import *

def problem():
    a = randint(11,100)
    b = randint(11,100)
    s = a*b
    return [f"{a} x {b}",s]

class ProblemGenerator(object):
    #have methods that return Questions and creates questions

    ### MULTIPLICATION PROBLEMS ###

    def random2x2(self):
        a = randint(11,100)
        b =randint(11,100)
        s = a*b
        return Question([a,b],f"{a} * {b}",s)

    def random3x3(self):
        a = randint(101, 1000)
        b = randint(101, 1000)
        s = a * b
        return Question([a,b],f"{a} * {b}",s)
    def square5(self):
        a = randrange(15,225,10)
        s = a**2
        return Question([a],f"{a} * {a}",s)

class Question(object): #container for all variables of a question one at a time
    def __init__(self,variables,prompt, solution, point_value=0, trick_desc='No description yet'):
        self.variables = variables
        self.prompt = prompt
        self.solution = solution
        self.point_value = point_value
        self.trick_desc = trick_desc
    #ex attributes: hint, prompt, solution, etc

def askQuestion(question): #handles using instances of Question
    pass