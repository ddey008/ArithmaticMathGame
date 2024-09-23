# Game Class essentially is the UI part for the game
# It does the button creation, resizing, scoreboard, restart, levels
# It passes the right variable to right methods and ensures functionality is a priority
import PIL as pil
import sympy as sp
import random as rand
import tkinter as tk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

from Mechanics import Mechanics
from Meth import Meth
import time
from sympy.core.sympify import SympifyError
import json
import os

from sympy.parsing.sympy_parser import parse_expr


class Game:

    # Constructor: Initializes user, level, score and best_score
    def __init__(self, user):
        # Sets the timer time in 300 seconds
        self.SCORE_FILE = "scores.json"
        self.timer = "05:00"
        self.answer_expr = None
        self.timer_time = 300
        self.user = user
        self.level = 0
        self.score = 0
        self.best_score = 0
        # Received this from Gimp
        self.initial_background_color = "#466965"
        self.image = pil.Image.open("calculus.png")
        self.total_questions = 1
        self.correct_answers = 0
        self.initial_question_x = 500
        self.initial_question_y = 30
        self.question_x = 500
        self.question_y = 30
        self.Mechanics = Mechanics(self.initial_question_x, self.initial_question_y, ground_level=700, max_y=0)
        self.pause = False
        self.past_question = None
        self.number_of_attempts = 1
        self.past_correct_answers = 0
        self.past_total_questions = 0
        self.past_no_of_attempts = 0
        self.end = None
        self.shouldresume= False

        # Creating the initial window
        self.create_window()

    def create_window(self):
        # Sets the title and Dimensions
        self.user.title("Calculus Game!")
        self.user.geometry("1000x700")

        # Opens the image and resizes it to a usable level and then uses Imagetk to fully make it a background
        self.image = self.image.resize((1000, 700), pil.Image.Resampling.LANCZOS)
        self.background_image = pil.ImageTk.PhotoImage(image=self.image)

        # Created the canvas to place the background image on
        self.my_canvas = tk.Canvas(self.user, width=1000, height=700)
        self.my_canvas.pack(fill="both", expand=True)

        # Actually doing the Background image placing part
        self.my_canvas.create_image(0, 0, anchor="nw", image=self.background_image)

        # Creating the buttons and Making them do the appropriate command
        self.button1 = tk.Button(self.user, text="Levels", bg=self.initial_background_color,
                                 command=self.create_level_windows)
        self.button2 = tk.Button(self.user, text="Best-Score", bg=self.initial_background_color, command=self.best_scores_window)
        self.button3 = tk.Button(self.user, text="Rules", bg=self.initial_background_color)

        # Creating the button windows on the canvas on top of the image
        button1_window = self.my_canvas.create_window(0, 0, anchor="nw", window=self.button1, height=55, width=100)
        button2_window = self.my_canvas.create_window(120, 0, anchor="nw", window=self.button2, width=100, height=55)
        button3_window = self.my_canvas.create_window(240, 0, anchor="nw", window=self.button3, width=100, height=55)

        # Banning the use of any sort of resizing
        self.user.resizable(width=False, height=False)

    def create_level_windows(self):
        # Creating the Level: Easy & Hard Windows
        self.easy_level_button = tk.Button(self.user, text="Easy", bg=self.initial_background_color,
                                           command=lambda: self.set_level(1))
        self.hard_level_button = tk.Button(self.user, text="Hard", bg=self.initial_background_color,
                                           command=lambda: self.set_level(2))

        # Putting the buttons on the canvas
        easy_button_window = self.my_canvas.create_window(0, 60, anchor="nw", window=self.easy_level_button, width=50,
                                                          height=40)
        hard_level_window = self.my_canvas.create_window(0, 110, anchor="nw", window=self.hard_level_button, width=50,
                                                         height=40)

    def set_level(self, level):
        self.level = level
        self.create_game_window()

    def best_scores_window(self):
        self.load_scores()

    # Initialize the Meth Stuff and create a TopLevel() for the second window and create the new window for the game. Also could implement back button after game finish
    def create_game_window(self):
        # Hiding the first window
        self.user.withdraw()
        self.load_scores()

        # Initialized the Meth object & Get the initial question in a string
        self.Math = Meth(self.level)

        self.question = self.Math.createquestion()
        print(sp.pretty(self.question))
        string = ""
        string += sp.pretty(self.question)

        ## Creating the image required to put into the rectangle box later
        self.create_question_image()

        # Window Stuff/ Lets just make a plain empty window with nothing right now

        # Creating the game_window with all the initialization
        self.second_window = tk.Toplevel()
        self.second_window.title("Game Window")
        self.second_window.geometry("1000x700")

        # No need for any Frames thus/ no need for pack and grid, just use Place

        # This doesn't work because there is a canvas of white color on top of the original window
        self.second_window['bg'] = "skyblue"

        # Creating the canvas required for rectangle object to drop
        self.game_canvas = tk.Canvas(self.second_window, width=1000, height=700, bg='SpringGreen2')
        self.game_canvas.pack(fill="both", expand=True)

        # Create the rectangle object in the canvas
        ## Question Location is important because it allows for the erasure self.question_location when it drops
        # self.rect = self.game_canvas.create_rectangle(400, 0, 600, 100, fill="#FF00FF")
        self.question_location = self.game_canvas.create_image(500, 30, image=self.question_image, anchor="center")

        # Add in the timer in the game window
        self.game_canvas.create_rectangle(0, 0, 100, 50)
        self.timer_text = self.game_canvas.create_text(40, 20, text=self.timer, fill="black",
                                                       font=("Times", 25, "bold"))

        self.second_window.resizable(height=False, width=False)

        # Creating the Score Part down at the bottom
        self.game_canvas.create_rectangle(0, 650, 100, 700)
        text = ""
        text += str(self.correct_answers) + "/" + str(self.total_questions)
        self.scoreboard = self.game_canvas.create_text(50, 675, text=text, fill="black", font=("Times", 25, "bold"))

        # Binding Mouse Keys to truly START THE GAME
        self.texter = self.game_canvas.create_text(500, 350, text="Click Anywhere To Start The Game!", fill="grey",
                                                   font=("Times", 30, "bold"))
        self.game_canvas.bind("<Button-1>", lambda event: self.startgame())

        self.second_window.protocol("WM_DELETE_WINDOW", self.end_game)

    def create_question_image(self):
        # The Latex equation needed for the image
        expr_latex = "$" + sp.latex(self.question) + "$"

        # Create Matplot figure to get the text
        fig, ax = plt.subplots(figsize=(1, 1))
        ax.text(0, 0, expr_latex, fontsize=20, ha='center', va='center')
        ax.axis('off')

        # Saving Figure In the images
        fig.savefig("temp.png", bbox_inches='tight', pad_inches=0, transparent=True)

        # Opening and doing the whole image rendering thing
        self.image1 = pil.Image.open("temp.png")
        self.question_image = pil.ImageTk.PhotoImage(self.image1)

    # Implement timer logic into the program
    # Implements GUI Logic into the program
    def timer_countdown(self):
        if self.timer_time > 0 and self.pause == False :
            minutes, seconds = divmod(self.timer_time, 60)
            self.timer = '{:02d}:{:02d}'.format(minutes, seconds)
            print(self.timer)
            self.timer_time -= 1
            self.game_canvas.itemconfig(self.timer_text, text=self.timer)
            # Schedule the next countdown update after 1000 milliseconds (1 second)
            self.second_window.after(1000, self.timer_countdown)
        elif self.timer_time<=0:
            self.texter2 = self.game_canvas.create_text(700, 150, text="Time's Up", fill="grey",
                                                       font=("Times", 30, "bold"))
            self.second_window.after(2000, lambda: self.game_canvas.delete(self.texter2))
            self.end_game()

    def startgame(self):
        # Delete the Click Anywhere to Start Text after 5.5 seconds
        self.second_window.after(0, lambda: self.game_canvas.delete(self.texter))

        # Create the Textbox to check the answer in the right location
        # Alternatively, I could make the text box appear after 1 second/ but that is too complicated
        # Throw in a label to show that is the answer box text
        self.input_text = tk.Text(self.second_window, height=10, width=20, font=("Roboto", 14), fg="black")
        self.input_text.place(x=90, y=250)

        # Make a button that allows the answer to be inputted
        self.answer_button = tk.Button(self.second_window, text="Answer", command=self.answer, font=("Times", 14))
        self.answer_window = self.game_canvas.create_window(200, 500, height=30, width=80, window=self.answer_button)
        # Sets off the timer
        self.timer_countdown()
        self.update()

    # Implements The Drop Logic using the Mechanics class
    def update(self):
        if self.Mechanics.ground_level >= self.question_y >= 0 and self.pause == False:
            self.Mechanics.update()
            self.game_canvas.move(self.question_location, 0, self.Mechanics.velocity)
            self.question_y = self.question_y + self.Mechanics.velocity
            print(self.question_y)
            self.second_window.after(1000, self.update)

        elif self.Mechanics.ground_level<= self.question_y:
            self.update_scoreboard(False)
            self.update_question()
            self.update()
        else:
            #Updates question twice, once when pause is true and once when it goes out of bounds
            self.update_question()

    def update_scoreboard(self, correctly_answered):
        text = ""
        print("Past Question:" + str(self.past_question))
        print("Current Question:" + str(self.question))
        if self.past_question != self.question:
            self.past_question = self.question
            if self.total_questions == 1 and correctly_answered == True and self.correct_answers == 0:
                self.correct_answers += 1

            elif self.total_questions == 1 and correctly_answered == False and self.number_of_attempts == 1:
                self.total_questions += 0

            elif correctly_answered == True:
                self.correct_answers += 1
                self.total_questions += 1

            elif correctly_answered == False:
                self.total_questions += 1
        self.number_of_attempts += 1
        print(self.number_of_attempts)
        text = str(self.correct_answers) + "/" + str(self.total_questions)
        self.game_canvas.itemconfig(self.scoreboard, text=text)

    def end_game(self):
        self.save_scores()
        self.answer_button.config(state=tk.DISABLED)
        self.pause = True

        self.game_canvas.create_text(700, 350, text="Do you Want To Save This Game For Later?", fill="grey",
                                     font=("Times", 23, "bold"))
        yes_button = tk.Button(self.second_window, text="Yes", command=lambda: self.resume(True) , font=("Times", 14))
        back_window = self.game_canvas.create_window(700, 400, height=30, width=50, window=yes_button)

        no_button = tk.Button(self.second_window, text="No", command=lambda: self.resume(False), font=("Times", 14))
        end_window = self.game_canvas.create_window(700, 450, height=30, width=50, window=no_button)

    def resume(self, choice):
        self.shouldresume = choice
        self.user.destroy()


    def pause_game(self):
        self.game_canvas.config(bg="#40B77B")
        self.pause = True
        self.game_canvas.bind("<Button-1>", lambda event: self.unpause_game())
        print("Paused")

    def unpause_game(self):
        self.second_window.after(0, lambda: self.game_canvas.delete(self.texter))
        self.game_canvas.config(bg="SpringGreen2")
        self.pause = False
        print("Unpaused")
        self.timer_countdown()
        self.update()

    # Gets any Existing Score from the Files
    def load_scores(self):
        if os.path.exists(self.SCORE_FILE):
            with open(self.SCORE_FILE, "r") as file:
                #This dictionary has a key and value pair and self.SCORE_FILE is just a file path loading all the data
                self.scores_data = json.load(file)
                if(self.scores_data["shouldresume"] == True):
                    self.correct_answers = self.scores_data["correct_answer"]
                    self.total_questions = self.scores_data["total_questions"]
                    self.number_of_attempts = self.scores_data["number_of_attempts"]
                    self.timer_time = self.scores_data["timer_time"]


                # It's assumed "scores.json" contains JSON data like {"user1": {"score": 100}}

    # Saves all the scores in the file
    def save_scores(self):
        scores_data = {
            "correct_answers": self.correct_answers,
            "total_questions": self.total_questions,
            "number_of_attempts": self.number_of_attempts,
            "timer_time": self.timer_time,
            "shouldresume": self.shouldresume
        }
        with open(self.SCORE_FILE, "w") as file:
            json.dump(scores_data, file)

    def update_question(self):
        # To Ensure no duplicate questions show up
        self.past_question = self.question
        self.question = self.Math.createquestion()

        if self.past_question != self.question:
            # Updating GUI part
            self.create_question_image()
            self.game_canvas.itemconfig(self.question_location, image=self.question_image)
            self.game_canvas.coords(self.question_location, self.initial_question_x, self.initial_question_y)
            self.question_y = self.initial_question_y

        else:
            self.update_question()

    # Checks if the answer is correct. If it is correct pause the game and show a new question?
    # Pausing means that the time stops, it gives out a big text called "Correct!Click to Unpause", the ui has a little bit of lighter green as everything is going on
    def answer(self):
        # Retrieves the user input in a string that is converted into sympy object
        answer_text = self.input_text.get("1.0", "end-1c")
        correct_ans = sp.simplify(self.Math.get_correctans(self.question))
        print("correct ans:" + str(correct_ans))
        answer_text = self.answer_string_correction(answer_text)

        # Create a try/Catch for error detection and telling the user their answer is incorrect
        try:
            self.answer_expr = sp.simplify(answer_text)
        except SympifyError:
            self.texter1 = self.game_canvas.create_text(700, 350, text="Incorrect Answer", fill="grey",
                                                        font=("Times", 30, "bold"))
            self.second_window.after(1500, lambda: self.game_canvas.delete(self.texter1))

        if (self.answer_expr != None):
            print("answer text:" + str(self.answer_expr))
            print(sp.simplify(self.answer_expr - correct_ans))
            # Since sometimes sympy simplify doesn't give the same answers, have them subtract each other
            # Ensure that correct and incorrect Answer is displayed in Gui
            if self.answer_expr.equals(correct_ans) or (sp.simplify(self.answer_expr - correct_ans) == 0):
                # self.texter is just deleted from canvas so you need to create a new text to make it work
                self.texter = self.game_canvas.create_text(700, 350, text="Correct! Click to Unpause", fill="grey",
                                                           font=("Times", 30, "bold"))
                print("Current Question:" + str(self.question))
                self.update_scoreboard(True)
                self.pause_game()
                self.update_question()
            else:
                self.texter1 = self.game_canvas.create_text(700, 350, text="Incorrect Answer", fill="grey",
                                                            font=("Times", 30, "bold"))
                self.second_window.after(1500, lambda: self.game_canvas.delete(self.texter1))
                self.update_scoreboard(False)

    def answer_string_correction(self, text):
        list = []
        text = text.replace(" ", "")
        text = text.replace("^", "**")
        text = text.lower()
        for i in range(len(text)):
            if (i + 1 != len(text)):
                if text[i].isdigit() and text[i + 1].isalpha():
                    text = text[:i + 1] + '*' + text[i + 1:]
                if text[i] == ")" and self.is_operator(text[i + 1]) == False:
                    text = text[:i + 1] + '*' + text[i + 1:]
        print(text)

        return text

    def is_operator(self, string):
        operators = ["*", "**", "+", "-", "^"]
        for i in operators:
            if (string == i):
                return True
        return False


if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()
