import tkinter as tk
from math import cos, sin
import threading
import time

x2s = []
y2s = []
thetas = []
colors = ["red", "green", "blue", "pink"]
threads = []


def main():
    root = tk.Tk()
    canvas = tk.Canvas(root, width=400, height=400)

    def on_click():
        def draw(n):
            while True:
                theta = thetas[n]
                x2 = x2s[n]
                y2 = y2s[n]
                canvas.create_line(200, 200, x2, y2, fill=colors[int(theta)//3 % 4])
                thetas[n] += 0.1
                theta = thetas[n]
                x2s[n] = cos(theta)*(200 - (n*124241214524542) % 50) + 200
                y2s[n] = sin(theta)*(200 - (n*124241214524542) % 50) + 200
                time.sleep(0.2 + (n*0.2*47540454542) % 0.2 - (n*0.2*4754322654621652) % 0.2)
        x2s.append(400)
        y2s.append(200)
        thetas.append(len(thetas)*0.14159718281828)
        thread = threading.Thread(target=lambda: draw(len(x2s)-1))
        thread.start()
        threads.append(thread)

    button = tk.Button(root, command=on_click, text='click me')
    canvas.pack()
    button.pack()
    root.mainloop()


if __name__ == '__main__':
    main()
