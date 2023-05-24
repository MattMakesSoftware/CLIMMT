### Command Line Interface Mental Math Training
### C.L.I.M.M.T.
### Matt Lombardi
from sys import argv
import random
import time
from datetime import timedelta

class User:
    usage = "C.L.I.M.M.T. usage: \npython3 CLIMMT.py [math mode] [number of problems] [timed (t or nt)] [include negative numbers (inclneg or posonly)] [add/sub range (lower-upper)] [mult/div range (lower-upper)]\n-math mode: include one or more of the following a - addition, s - subtraction, m - multiplication, d - division"
    example = "Example: python3 CLIMMT.py asm 15 nt inclneg 0-20 0-12"
    def __init__(self, inputs):
        if len(inputs) < 7:
            print(self.usage)
            print(self.example)
            exit()
        self.mathmode = inputs[1]
        self.problem_amount = inputs[2]
        self.timed = inputs[3]
        self.allow_negatives = inputs[4]
        self.add_sub_range = inputs[5]
        self.mult_div_range = inputs[6]
        self.answers = []
        self.score = 0
    
    @property    
    def mathmode(self):
        return self._mathmode
    
    @mathmode.setter
    def mathmode(self, mathmode):
        if len(mathmode) > 4 or set(mathmode).isdisjoint({"a", "s", "m", "d"}):
            print("First argument must include one or a combination of a, s, m , and/or d to signifiy addition, subtraction, multiplication, and/or division")
            print(self.usage)
            exit()   
        self._mathmode = mathmode
        
    @property
    def problem_amount(self):
        return self._problem_amount
    
    @problem_amount.setter
    def problem_amount(self, problem_amount):
        try:
            int(problem_amount)
        except ValueError:
            print("Second argument must be a positive integer less than 100 to signify the number of problems")
            print(self.usage)
            exit()
        if not 0 < int(problem_amount) < 100:
            print("Second argument must be a positive integer less than 100")
            print(self.usage)
            exit()
        self._problem_amount = problem_amount
    
    @property
    def timed(self):
        return self._timed
    
    @timed.setter
    def timed(self, timed):
        if timed not in ["t", "nt"]:
            print("Third argument must be either 't' or 'nt' to signify 'timed' or 'not timed'")
            print(self.usage)
            exit()
        self._timed = timed
    
    @property
    def allow_negatives(self):
        return self._timed
    
    @allow_negatives.setter
    def allow_negatives(self, allow_negatives):
        if allow_negatives not in ["inclneg", "posonly"]:
            print("Fourth argument must be either 'inclneg' or 'posonly' to signify 'include negative numbers' or 'positive numbers only'")
            print(self.usage)
            exit()
        self._allow_negatives = allow_negatives
        
    @property
    def add_sub_range(self):
        return self._add_sub_range
    
    @add_sub_range.setter
    def add_sub_range(self, add_sub_range):
        try:
            add_sub_range = add_sub_range.split("-")
            int(add_sub_range[0])
            int(add_sub_range[1])
            if len(add_sub_range) != 2 or int(add_sub_range[0]) < 0 or int(add_sub_range[1]) < 0 or int(add_sub_range[0]) > int(add_sub_range[1]):
                raise Exception()
        except Exception:
            print("Fifth argument must be a range of non-negative integers denoted by '[lower bound]-[upper bound]' to show range of addition/subtraction problems")
            print(self.usage)
            exit()
        self._add_sub_range = add_sub_range
        
    @property
    def mult_div_range(self):
        return self._mult_div_range
    
    @mult_div_range.setter
    def mult_div_range(self, mult_div_range):
        try:
            mult_div_range = mult_div_range.split("-")
            int(mult_div_range[0])
            int(mult_div_range[1])
            if len(mult_div_range) != 2 or int(mult_div_range[0]) < 0 or int(mult_div_range[1]) < 0 or int(mult_div_range[0]) > int(mult_div_range[1]):
                raise Exception()
        except Exception:
            print("Sixth argument must be a range of non-negative integers denoted by '[lower bound]-[upper bound]' to show range of multipication/division problems")
            print(self.usage)
            exit()
        self._mult_div_range = mult_div_range
        
    def update_answers(self, newscore):
        self.answers.append(newscore)
        
    def update_score(self):
        self.score += 1
        


def main():
    #start program, get and store user inputs, show usage if incomplete
    player = User(argv)
    #display settings for Mental Math Practice run, prompt user to start
    initialize_CLIMMT(player)
    start_CLIMMT()
    math_training(player)
    show_results(player)

#do the mental math practice run 
def math_training(player):
    input("Press Enter to begin\n")
    if player.timed == "t":
        start = time.time()
    for i in range(int(player.problem_amount)):
        print(f"Problem {i + 1}:")
        probnums, operand, user_answer, answer_correct, correct_answer = math_problem(player.mathmode, player.allow_negatives, player.add_sub_range, player.mult_div_range)
        if answer_correct:
            player.update_score()
        player.update_answers([i + 1, f"{probnums[0]} {operand} {probnums[1]} = {correct_answer}", user_answer])
    print(f"Math Training Complete. Final Score: {player.score}/{player.problem_amount}")
    if player.timed == "t":
        end = time.time()
        diff = end-start
        tdiff = timedelta(seconds= diff)
        seconds = tdiff.total_seconds()
        minutes = 0
        if seconds > 60:
            minutes = int(seconds / 60)
        print(f"Time: {minutes} minutes, {seconds:.2f} seconds")
        
        
def math_problem(mathmodes, allow_negatives, add_sub_range, mult_div_range):
    #select random letter representing the up to 4 possible problems
    currentmode = random.choice(mathmodes)
    if currentmode == "a":
        numbers = select_range(add_sub_range, allow_negatives)
        correct_answer, *probnums = add_problem(numbers)
        user_answer, operand = prompt_user(probnums, "+")
    elif currentmode == "s":
        numbers = select_range(add_sub_range, allow_negatives)
        correct_answer, *probnums = subtract_problem(numbers)
        user_answer, operand = prompt_user(probnums,"-")
    elif currentmode == "m":
        numbers = select_range(mult_div_range, allow_negatives)
        correct_answer, *probnums = multiply_problem(numbers)
        user_answer, operand = prompt_user(probnums, "•")
    elif currentmode == "d":
        numbers = select_range(mult_div_range, allow_negatives)
        correct_answer, *probnums = divide_problem(numbers)
        user_answer, operand = prompt_user(probnums, "/")
    if str(user_answer).lower() == str(correct_answer).lower():
        answer_correct = True
    else: answer_correct = False
    return probnums, operand, user_answer, answer_correct, correct_answer


def prompt_user(probnums, operand):
    user_answer = input(f"{probnums[0]} {operand} {probnums[1]}\n")
    return user_answer, operand

def add_problem(numbers):
    firstnumber, secondnumber = numbers
    answer = firstnumber + secondnumber
    return answer, firstnumber, secondnumber
def subtract_problem(numbers):
    secondnumber, answer = numbers
    firstnumber = secondnumber + answer
    return answer, firstnumber, secondnumber
    
def multiply_problem(numbers):
    firstnumber, secondnumber = numbers
    answer = firstnumber * secondnumber
    return answer, firstnumber, secondnumber
    
def divide_problem(numbers):
    secondnumber, answer = numbers
    firstnumber = secondnumber * answer
    if secondnumber == 0:
        answer  = "undefined"
    return answer, firstnumber, secondnumber
    
def select_range(range, negative):
    firstposnumber = random.randrange(int(range[0]), int(range[1]))
    secondposnumber = random.randrange(int(range[0]), int(range[1]))
    if negative == "inclneg":
        firstnegnumber = random.randrange(-int(range[1]), -int(range[0]))
        secondnegnumber = random.randrange(-int(range[1]), -int(range[0]))
        firstnumber = random.choice([firstposnumber, firstnegnumber])
        secondnumber = random.choice([secondposnumber, secondnegnumber])
    else:
        firstnumber = firstposnumber
        secondnumber = secondposnumber
    return firstnumber, secondnumber
      
#display score and prompt to review problem/ answers
def show_results(player):
    results = input("Show results? (y/n)\n")
    if results.lower() == "n":
        exit()
    for answer in player.answers:
        print(f"\nProblem: {answer[0]}\n{answer[1]}, User Answer: {answer[2]}")
    input("\nPress enter to quit")
    exit()
    
#start the math training
def initialize_CLIMMT(player):
    modes = []
    possiblemodes = {"a": "Addition", "s": "Subtraction", "m": "Multiplication", "d": "Division"}
    for mode in {*player.mathmode}:
        for letter in possiblemodes:
            if mode == letter:
                modes += [possiblemodes[letter]]
    mathmodes = ", ".join(modes)
    if player.timed == "t":
        timed = "Timed"
    else: timed = "Untimed"
    if player.allow_negatives == "inclneg":
        negatives = "Negative Numbers Included"
    else: negatives = "Negative Numbers Not Included"
    print("\n~Command Line Interface Mental Math Training (C.L.I.M.M.T)~")
    print("############################################################")
    print("C.L.I.M.M.T. Settings:")
    print(f"Math Mode: {mathmodes}")
    print(f"Number of problems: {player.problem_amount}")
    print(f"{timed}")
    print(f"{negatives}")
    print(f"Range of Addition/Subtraction Problems: {'-'.join(player.add_sub_range)}")
    print(f"Range of Multiplication/Division Problems: {'-'.join(player.mult_div_range)}")
    print("############################################################")

def start_CLIMMT():
    begin = input("Enter Y to confirm selection, enter Q to quit\n")
    if begin.upper() == "Y":
        return
    elif begin.upper() == "Q":
        exit()
    else: 
        start_CLIMMT()
        return

if __name__ == "__main__":
    main()