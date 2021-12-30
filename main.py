import tkinter as tk
import random
import time
Refresh_Sec = 0.005
Ball_min_movement = 1

colors = ['red', 'green', 'yellow', 'blue']

class Ball:
    def __init__(self, can):
        self.can = can
        self.radius = 25
        self.x = random.randint(0,500)
        self.y = random.randint(0,500)
        self.ball = can.create_oval(self.x, self.y, self.x + self.radius, self.y + self.radius, fill='red', outline='white')
        self.shift_x = Ball_min_movement
        self.shift_y = Ball_min_movement
        self.ball_in_motion = False
        self.color = colors[0]

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
        x1, y1, x2, y2 = ball_pos
        if x1 < 0 or x2 > self.can.winfo_width():
            self.shift_x = - self.shift_x
            self.change_color()
        if y1 <0 or y2 > self.can.winfo_height():
            self.shift_y = - self.shift_y
            self.change_color()

    def play(self):
        self.ball_in_motion = True
        while self.ball_in_motion:
            self.motion()

    def stop(self):
        self.ball_in_motion = False

window = tk.Tk()
window.title("Pinball")
frame = tk.Frame(window)
frame.pack(side=tk.TOP)

can = tk.Canvas(window, bg='black', height=600, width=500)
can.pack(side=tk.TOP, padx=5, pady=5)

ball = Ball(can)
btn = tk.Button(frame, text='Play', command=ball.play)
btn.pack()
btn2 = tk.Button(frame, text='Stop', command=ball.stop)
btn2.pack()
can.update()

window.mainloop()
