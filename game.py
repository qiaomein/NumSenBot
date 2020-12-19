
import discord
from fractions import Fraction
from random import *

class ProblemGenerator(object):
    #have methods that return Questions and creates questions
    def __init__(self):
        pass
    ### MULTIPLICATION PROBLEMS ###

    def random2x2(self):
        a = randint(11,100)
        b = randint(11,100)
        s = a*b
        return Question([a,b],f"{a} * {b}",s)

    def random3x3(self):
        a = randint(101, 1000)
        b = randint(2,10)
        s = a * b
        return Question([a,b],f"{a} * {b}",s)
    def square5(self):
        a = randrange(15,225,10)
        s = a**2
        return Question([a],f"{a} * {a}",s)

    def near100(self):
        a = randint(90,110)
        b = randint(90,110)
        return Question([a,b],f'{a} * {b}', a*b)

    def reverses(self):
        a = randint(12,100)
        b = int(str(a)[::-1])
        return Question([a,b],f'{a} * {b}', a*b)

    def square50(self):
        a = randint(41, 59)
        return Question([a], f'{a} * {a}', a ** 2)

    ### FRACTION PROBLEMS ###

    def reciprocal(self):
        a1 = randint(2,10)
        b1 = randint(2,10)
        a = Fraction(a1, b1)
        b = Fraction(b1, a1)
        return Question([a],f'\\frac{{{a.numerator}}}{{{a.denominator}}} + \\frac{{{a.denominator}}}{{{a.numerator}}}', (a+b).limit_denominator(max_denominator=500))

    ### MISC ###
    def unitsdigit(self):
        a = randint(8,45)
        b = randint(10,50)
        return Question([a,b], f'{a} ^ {{{b}}}', str(a**b)[-1])

class Question(object): #container for all variables of a question one at a time
    def __init__(self,variables,prompt, solution, point_value=0, trick_desc='No description yet', type = ''):
        self.variables = variables
        self.prompt = prompt
        self.solution = solution
        self.point_value = point_value
        self.trick_desc = trick_desc
        self.type = type
    #ex attributes: hint, prompt, solution, etc
