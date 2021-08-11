import time
import tkinter as tk
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
from client_server import Client
import os


def get_animated_plot(corridor, plot_name, data_filename, root):
    # Create figure for plotting
    fig, ax = plt.subplots()
    xs = []
    ys = []

    def animate(i, xs: list, ys: list):
        try:
            with open(data_filename, 'r') as file:
                data = file.read()
        except:
            with open(data_filename, 'w') as file:
                pass

        try:
            flt = float(data.split("__")[0])
        except:
            flt = float(data.split("__")[1])
        # Add x and y to lists
        xs.append(str(time.time())[5:])
        ys.append(flt)
        xs = xs[-10:]
        ys = ys[-10:]
        # Draw x and y lists
        ax.clear()
        ax.plot(xs, ys)
        # Format plot
        ax.set_ylim([corridor[0], corridor[1]])
        ax.set_title(plot_name)
        fig.autofmt_xdate(bottom=0.3, rotation=45, ha='right')
        ax.set_ylabel('Данные с датчика')
        ax.set_xlabel('Время')
        print(flt)

    bar1 = FigureCanvasTkAgg(fig, root)
    bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

    return animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=3000)


# root = tk.Tk()
#
# ani1 = get_animated_plot([0,100],'dht_11_wet', 'dht_11_wet', root)
# time.sleep(1)
# ani2 = get_animated_plot([20, 40],'dht_11_temp', 'dht_11_temp', root)
# time.sleep(1)
# ani3 = get_animated_plot([0, 3500],'light_sensor', 'light_sensor', root)
# time.sleep(1)
#
# root.mainloop()
# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/

import tkinter as tk

LARGE_FONT = ("Verdana", 12)


class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        self.title('SCS')
        self.geometry('1920x1080')

        self.server_started = False

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

        self.anim = []

        self.animation_not_started_yet = True

    def show_frame(self, cont):
        if cont == PageTwo:
            os.system('start cmd /c python client_server.py')
            self.server_started = True
            if self.animation_not_started_yet:
                frame = self.frames[cont]
                frame.tkraise()
                frame.start_animation(self)
                self.animation_not_started_yet = False
            else:
                frame = self.frames[cont]
                frame.tkraise()
                frame.continue_animation(self)


        else:
            if self.server_started:
                os.system("taskkill /im cmd.exe")
            frame = self.frames[cont]
            frame.tkraise()
            frame = self.frames[PageTwo]
            frame.terminate_animation(self)
            print('anim terminated')


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Главная страница", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button2 = tk.Button(self, text="Автобусная остановка",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        button = tk.Button(self, text="О проекте",
                           command=lambda: controller.show_frame(PageOne))
        button.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="О проекте", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        label = tk.Label(self, text="Тут должен быть очень длинный текст с описанием проекта\n"
                                    "Но мне его очень лень писать, к тому же, его вряд ли \n"
                                    "Кто либо будет читать")
        label.pack()

        button1 = tk.Button(self, text="На главную",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Автобусная остановка", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="На главную",
                            command=lambda: controller.show_frame(StartPage))

        button1.pack()

    def start_animation(self, parent):

        parent.anim.append(get_animated_plot([0, 100], 'Датчик влажности', 'dht_11_wet', self))
        parent.anim.append(get_animated_plot([20, 40], 'Датчик температуры', 'dht_11_temp', self))
        parent.anim.append(get_animated_plot([0, 3500], 'Датчик света', 'light_sensor', self))

    def terminate_animation(self, parent):

        try:
            for i in parent.anim:
                i.event_source.stop()
            print('stopped')
        except Exception as ex:
            print('error in stopping')
            print(ex)
            pass

    def continue_animation(self, parent):

        try:
            for i in parent.anim:
                i.event_source.start()
            print('stopped')
        except Exception as ex:
            print('error in stopping')
            print(ex)
            pass


app = SeaofBTCapp()
app.mainloop()
