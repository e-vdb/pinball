import tkinter as tk
import random
import time
from stopwatch import StopWatch
Refresh_Sec = 0.005
Ball_min_movement = 1
colors = ['red', 'green', 'yellow', 'blue']


class Ball:
    def __init__(self, can, bar):
        self.can = can
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
        time.sleep(Refresh_Sec)
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
        self.x = 100
        self.y = 550
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

class Game:
    def __init__(self, window, can, label):
        self.window = window
        self.can = can
        self.label = label
        self.bar = Bar(self.can)
        self.ball = Ball(self.can, self.bar)
        self.sw = StopWatch(window)
        self.sw.pack(side=tk.TOP)

    def new_game(self):
        self.sw.Reset()
        self.label.configure(text='Keep the ball in motion!!!')
        self.ball.ball_in_motion = True
        self.sw.Start()
        if self.ball.ball_in_motion:
            self.ball.play()
        self.game_over()

    def game_over(self):
        self.label.configure(text='Game over. Click on play to try again.')
        self.sw.Stop()


window = tk.Tk()
window.title("Moving ball")
frame = tk.Frame(window)
frame.pack(side=tk.TOP)
can = tk.Canvas(window, bg='black', height=600, width=500)
can.pack(side=tk.TOP, padx=5, pady=5)
lab_Message = tk.Label(frame, text="Click on Play to start the game", fg="black", font='Helvetica 14')
lab_Message.pack(side=tk.TOP)

game = Game(window, can, lab_Message)
btn = tk.Button(frame, text='Play', command=game.new_game)
btn.pack()

can.update()
window.bind("<Left>", game.bar.move_left)
window.bind("<Right>", game.bar.move_right)
window.mainloop()
