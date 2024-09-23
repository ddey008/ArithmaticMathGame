import sympy as simp
import random as rand
class Meth:

    # Need to hold all possible permutations of questions
    def __init__(self, level):
        self.x, self.a = simp.symbols('x a ')
        self.level = level # Can be 1(Easy),2(Not Easy)
        self.functions = ["Constant", "Polynomial", "Trig", "Inverse Trig", "Exponential Power"]
        self.string = ""

    # Need to use level field to ensure the proper level of hardness
    # The functions uses randint to get a number that is then used to choose one of functions from array
    #
    def createquestion(self):
        expression = 0
        chooser = -1
        if self.level == 1:
            for i in range(2):
                choice = rand.randint(0, 2)
                if chooser != choice:
                    chooser = choice
                    expression += self.switch_case(choice)
                else:
                    while(choice==chooser):
                        choice = rand.randint(0, 2)
                    chooser=choice
                    expression+=self.switch_case(choice)

        elif(self.level == 2):
            for i in range(2):
                choice = rand.randint(0, 4)
                expression += self.switch_case(choice)
        print(expression)
        return expression

    def switch_case(self, value):
        if(value == 0):
            return self.create_constant()
        elif(value==1):
            return self.create_polynomial()
        elif(value==2):
            return self.create_trig()
        elif(value==3):
            return self.create_inversetrig()
        elif(value==4):
            return self.create_exponential()
    def create_constant(self):
        return rand.randint(1,10)

    def create_polynomial(self):
        power = rand.randint(1,5)
        coefficient = rand.randint(1,10)
        expression = coefficient * self.x ** power
        return expression # Since expression has self.x or symbolic sympy, expression becomes a sympy object

    def create_trig(self):
        trig_functions = [simp.cos(self.x), simp.sin(self.x), simp.tan(self.x), simp.cot(self.x), simp.csc(self.x), simp.sec(self.x)]
        power = rand.randint(1, 2)
        coefficient = rand.randint(1, 10)
        expression = coefficient * rand.choice(trig_functions)**power
        return expression

    def create_inversetrig(self):
        inverse_func = [simp.acos(self.x), simp.asin(self.x), simp.atan(self.x)]
        coefficient = rand.randint(1, 10)
        expression = coefficient * rand.choice(inverse_func)
        return expression

    def create_exponential(self):
        exponential = [self.a ** self.x, simp.exp(self.x), simp.log(self.x) ]
        power = rand.randint(1, 2)
        coefficient = rand.randint(1, 10)
        expression = coefficient*rand.choice(exponential)**power
        return expression
    #Returns the correct answer
    def get_correctans(self,expression):
        derivative = simp.diff(expression, self.x)
        return derivative

    # Returns the string version of the question
    def get_question_string(self,expression):
        return simp.pretty(expression)

    # Returs the string version of the answer
    def get_answer_string(self, expression):
        return simp.pretty(expression)
'''
def test_meth():
    for level in [1, 2]:
        meth = Meth(level)
        expression = meth.createquestion()
        derivative = simp.diff(expression, meth.x)

        # Print the results
        print(f"Level {level} Question: {expression}")
        print(f"Level {level} Derivative: {derivative}")
        print("\nPretty Print Expression:")
        print(simp.pretty(expression))
        print("\nPretty Print Derivative:")
        print(simp.pretty(derivative))
        print("\n" + "-" * 50 + "\n")


# Run the tester function
test_meth()
'''