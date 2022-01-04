import tkinter as tk
import random
import time
from stopwatch import StopWatch
from help_functions import about, printRules
from high_scores import Score
Refresh_Sec = 0.005
Ball_min_movement = 1
colors = ['red', 'green', 'yellow', 'blue']


class Ball:
    def __init__(self, can, bar, refresh_Sec=Refresh_Sec):
        self.can = can
        self.refresh_Sec = refresh_Sec
        self.radius = 25
        self.x = random.randint(5,490)
        self.y = 0
        self.ball = can.create_oval(self.x, self.y, self.x + self.radius, self.y + self.radius,
                                    fill='red', outline='white')
        self.shift_x = Ball_min_movement
        self.shift_y = Ball_min_movement
        self.ball_in_motion = False
        self.color = colors[0]
        self.bar = bar

    def reset(self):
        self.x = random.randint(0,500)
        self.y = 0
        self.can.delete(self.ball)
        self.ball = can.create_oval(self.x, self.y, self.x + self.radius, self.y + self.radius, fill='red',
                                    outline='white')

    def change_color(self):
        index_color = colors.index(self.color)
        if index_color < len(colors) - 1:
            self.color = colors[index_color + 1]
        else:
            self.color = colors[0]
        self.can.itemconfig(self.ball, fill=self.color)

    def motion(self):
        self.can.move(self.ball, self.shift_x, self.shift_y)
        self.can.update()
        time.sleep(self.refresh_Sec)
        ball_pos = self.can.coords(self.ball)
        bar_x1, bar_y1, bar_x2, bar_y2 = self.can.coords(self.bar.bar)
        x1, y1, x2, y2 = ball_pos
        if y2 == bar_y2:
            if (bar_x1 <= x1 <= bar_x2) or (bar_x1 <= x2 <= bar_x2):
                self.shift_y = - self.shift_y
        elif y1 < 0:
            self.shift_y = - self.shift_y
            self.change_color()
        elif y2 > self.can.winfo_height():
            self.stop()
        if x1 < 0 or x2 > self.can.winfo_width():
            self.shift_x = - self.shift_x
            self.change_color()

    def play(self):
        self.reset()
        self.ball_in_motion = True
        while self.ball_in_motion:
            self.motion()

    def stop(self):
        self.ball_in_motion = False
        self.can.delete(self.ball)


class Bar:
    def __init__(self, can):
        self.can = can
        self.width = 50
        self.height = 10
        print(self.can.winfo_width())
        self.x = (self.can.winfo_width() - self.width) / 2
        self.y = 550
        self.bar = self.can.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height,
                                             fill='white', outline='white')

    def center_bar(self):
        self.can.delete(self.bar)
        self.x = (self.can.winfo_width() - self.width) / 2
        self.bar = self.can.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height,
                                             fill='white', outline='white')

    def move_right(self, event):
        x1, _, x2, _ = self.can.coords(self.bar)
        if x2 + 10 < self.can.winfo_width():
            self.can.move(self.bar, 10, 0)

    def move_left(self, event):
        x1, _, x2, _ = self.can.coords(self.bar)
        if x1 - 10 > 0:
            self.can.move(self.bar, -10, 0)


class Player:
    def __init__(self):
        self.can_play = False
        self.name = 'unknown'

    def enter_name(self):
        self.name_window = tk.Toplevel()
        lbl_enter_name = tk.Label(self.name_window, text="Enter your name", fg="black")
        lbl_enter_name.pack()
        ent_name = tk.Entry(self.name_window)
        ent_name.insert(0, 'Player')
        ent_name.pack()
        btn_enter_name = tk.Button(self.name_window, text="Enter",
                                   command=lambda: self.enter(ent_name))
        btn_enter_name.pack()

    def enter(self, name):
        self.name = name.get()
        self.name_window.destroy()
        self.can_play = True


class Game:
    def __init__(self, window, can, label):
        self.window = window
        self.can = can
        self.label = label
        self.can.update()
        self.bar = Bar(self.can)
        self.ball = Ball(self.can, self.bar)
        self.sw = StopWatch(window)
        self.sw.pack(side=tk.TOP)
        self.score = Score()
        self.score.load_score()
        self.player = Player()


    def set_difficulty_level(self, option):
        if option == 0:
            self.ball.refresh_Sec = 0.005
        elif option == 1:
            self.ball.refresh_Sec = 0.0025
        else:
            self.ball.refresh_Sec = 0.00175

    def play(self):
        self.sw.Reset()
        self.bar.center_bar()
        if self.player.can_play:
            self.label.configure(text='Keep the ball in motion!!!')
            self.ball.ball_in_motion = True
            self.sw.Start()
            if self.ball.ball_in_motion:
                self.ball.play()
            self.game_over()

    def new_game(self):
        self.sw.Reset()
        self.bar.center_bar()
        self.player.enter_name()
        self.label.configure(text='Click on play to start the game.')

    def game_over(self):
        self.label.configure(text='Game over. Click on play to try again.')
        self.sw.Stop()
        self.score.add_score(self.player.name, self.sw._elapsedtime)

    def show_stat(self):
        self.stat_window = tk.Toplevel()
        self.stat_window.title("Statistics")
        self.stat_window.resizable(False, False)
        stat = self.score.df.head()
        lab_stat = tk.Label(self.stat_window, text=stat, fg="black", font='Helvetica 12')
        lab_stat.pack(side=tk.TOP)
        btn_reset = tk.Button(self.stat_window,
                              text="Reset", fg="red", font='Arial 15',
                              command=self.score.erase_score)
        btn_reset.pack()
        self.stat_window.mainloop()



window = tk.Tk()
window.title("Moving ball")
frame = tk.Frame(window)
frame.pack(side=tk.TOP)
can = tk.Canvas(window, bg='black', height=600, width=500)
can.pack(side=tk.TOP, padx=5, pady=5)
lab_Message = tk.Label(frame, text="Click on Game to start a new game", fg="black", font='Helvetica 14')
lab_Message.pack(side=tk.TOP)
game = Game(window, can, lab_Message)
#Menus
top = tk.Menu(window)
window.config(menu=top)

game_menu = tk.Menu(top, tearoff=False)
top.add_cascade(label='Game', menu=game_menu)
game_menu.add_command(label='New game', command=game.new_game)
game_menu.add_command(label='Exit', command=window.destroy)

option_menu = tk.Menu(top, tearoff=False)
top.add_cascade(label='Difficulty', menu=option_menu)
option_menu.add_command(label='Easy', command=lambda x=0: game.set_difficulty_level(x))
option_menu.add_command(label='Intermediate', command=lambda x=1: game.set_difficulty_level(x))
option_menu.add_command(label='Difficult', command=lambda x=2: game.set_difficulty_level(x))

help_menu = tk.Menu(top, tearoff=False)
top.add_cascade(label='Help', menu=help_menu)
help_menu.add_command(label='How to play?', command=printRules)
help_menu.add_command(label='About', command=about)




btn = tk.Button(frame, text='Play', command=game.play)
btn.pack()
score_menu = tk.Menu(top, tearoff=False)
top.add_cascade(label='Score', menu=score_menu)
score_menu.add_command(label='High scores', command=game.show_stat)
#can.update()
window.bind("<Left>", game.bar.move_left)
window.bind("<Right>", game.bar.move_right)

window.mainloop()
