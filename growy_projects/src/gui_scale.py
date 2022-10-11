import random
import tkinter
import tkinter.messagebox
import customtkinter
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import serial as sr
import time

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"
ser = sr.Serial('/dev/serial0', 9600, timeout=1)

class GraphFigure():
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.data = np.array([])

    def animate(self, i):
        ser.reset_input_buffer()
        ser.write("weight\n".encode())
        b = ser.readline()
        b.decode()
        print(b)

        # replacement for serial data
        # a = random.randint(500, 5000)

        self.ax.cla()
        self.ax.set_xticks([])
        self.ax.set_title('gutter scale')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('weight(g)')
        self.ax.set_ylim(-0.5, 5000)
        self.ax.set_yticks([0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000])
        if b == b'':
            print("no serial data")
            return
        else:
            if (len(self.data) < 100):
                self.data = np.append(self.data, float(b[0:4])) # ser data
                print(self.data)
            else:
                self.data[0:99] = self.data[1:100]
                self.data[99] = float(b[0:4])
            self.ax.plot(np.arange(0, len(self.data)), self.data)

class SideBar(customtkinter.CTk):

    def __init__(self, parent):
        self.parent = parent
        self.frame = customtkinter.CTkFrame(master=self.parent, width=180, corner_radius=0)

        # configure grid layout (1x11)
        self.frame.grid_rowconfigure(0, minsize=10)  # empty row with minsize as spacing
        self.frame.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame.grid_rowconfigure(8, minsize=20)  # empty row with minsize as spacing
        self.frame.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label = customtkinter.CTkLabel(master=self.frame,
                                            text="Scale graphs",
                                            text_font=("Roboto Medium", -16))  # font name and size in px
        self.label.grid(row=1, column=0, pady=10, padx=10)

        self.weigh_bttn = customtkinter.CTkButton(master=self.frame,
                                                  text="weigh gutter",
                                                  state="disabled",
                                                  text_font=("Roboto Medium", 8),
                                                  command=self.button_event)
        self.weigh_bttn.grid(row=2, column=0, pady=10, padx=20)

        self.callibrate_bttn = customtkinter.CTkButton(master=self.frame,
                                                       text="Callibrate",
                                                       state='normal',
                                                       text_font=("Roboto Medium", 10),
                                                       command=self.button_event)
        self.callibrate_bttn.grid(row=3, column=0, pady=10, padx=20)

        self.label_mode = customtkinter.CTkLabel(master=self.frame, text="Appearance Mode:", text_font=("", 9))
        self.label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame,
                                                        values=["Light", "Dark", "System"],
                                                        command=self.change_appearance_mode)
        self.optionmenu_1.grid(row=10, column=0, pady=10, padx=20, sticky="w")

    def button_event(self):
      self.parent.change_page()

    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

class CalibrateScreen(customtkinter.CTk):
    def __init__(self, parent):
        self.parent = parent
        self.frame = customtkinter.CTkFrame(master=self.parent, fg_color='grey', corner_radius=0)
        self.frame.grid(row=0, column=1, sticky="nswe")
        self.frame.grid_rowconfigure(0, minsize=200)   # empty row with minsize as spacing
        self.frame.grid_rowconfigure(3, minsize=50)  # empty row as spacing
        self.frame.grid_rowconfigure(5, weight=1)    # empty row with minsize as spacing

        self.border_color = customtkinter.CTkFrame(master=self.frame, fg_color='#68DB95', corner_radius=10)
        self.border_color.grid(row=0, column=2, pady=5, padx=5)
        self.weight_data = customtkinter.CTkLabel(master=self.border_color,
                                                  text="",
                                                  text_font=("Roboto Medium", 10))
        self.weight_data.grid(row=0, column=2, pady=5, padx=5)

        self.text1 = customtkinter.CTkLabel(master=self.frame,
                                            text=" first calibrate the load-sensors and then tare!")
        self.text1.grid(row=1, column=1, pady=5, padx=5)

        self.calibrate_bttn = customtkinter.CTkButton(master=self.frame,
                                                text="calibrate",
                                                text_font=("Roboto Medium", 10),
                                                command=self.calibrate_it)
        self.calibrate_bttn.grid(row=2, column=1, pady=10, padx=20)
        self.loadcell_R = customtkinter.CTkLabel(master=self.frame,
                                            text_font=("Roboto Medium", 10))
        self.loadcell_L = customtkinter.CTkLabel(master=self.frame,
                                            text_font=("Roboto Medium", 10))
        self.tare_bttn = customtkinter.CTkButton(master=self.frame,
                                                text="Tare",
                                                text_font=("Roboto Medium", 10),
                                                command= self.tare_it)
        self.tare_bttn.grid(row=4, column=1, pady=10, padx=20)
        self.tare_label = customtkinter.CTkLabel(master=self.frame, text="")
        self.show_weight()

    def show_weight(self):
        # ser.reset_input_buffer()
        # ser.write("weight\n".encode())
        # self.weight = ser.readline()
        # # a = random.randint(500, 5000)
        # self.weight_data.configure(text= self.weight)
        # self.weight_data.after(1000, self.show_weight)
        return 0

    def calibrate_it(self):
        # ser.reset_input_buffer()
        # ser.write("zero\n".encode())
        # self.weight= ser.readline()
        # # self.calibrate= "R159897 L185236\n"
        # raw_loadcell = self.weight.split()
        # self.loadcell_R.configure(text=raw_loadcell[0])
        # self.loadcell_L.configure(text=raw_loadcell[1])
        # self.loadcell_R.grid(row=2, column=2, pady=5, padx=5)
        # self.loadcell_L.grid(row=2, column=3, pady=5, padx=5)
        # self.loadcell_R.after(2000, self.rm_calibrate_labels)
        return 0

    def tare_it(self):
        # ser.reset_input_buffer()
        # ser.write("tare\n".encode())
        # self.tare= ser.readline()
        # self.tare.decode()
        # # self.tare= "0.01\n"
        #
        # if self.tare == "0.00\n":
        #     self.tare_label.configure(text="weight scale is tared : " + str(self.tare) + " g")
        # else:
        #     self.tare_label.configure(text="weight scale is not tared, serial error! ( output: " + str(self.tare)+")")
        #
        # self.tare_label.grid(row=4, column=2, pady=5, padx=5)
        # self.tare_label.after(2000, self.rm_tare_label)
     return 0

    def rm_tare_label(self):
        self.tare_label.grid_remove()

    def rm_calibrate_labels(self):
        self.loadcell_R.grid_remove()
        self.loadcell_L.grid_remove()





class WeighGutterScreen(customtkinter.CTk):
    def __init__(self, parent):
        self.parent = parent
        self.frame = customtkinter.CTkFrame(master=self.parent, fg_color='grey', corner_radius=0)
        self.frame.grid(row=0, column=1, sticky="nswe")
        self.graph = GraphFigure()
        # ===== display figure =====
        self.canvas = FigureCanvasTkAgg(self.graph.fig, master=self.frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, pady=40, padx=40)

        self.start_animate_fig()

        self.messure_bttn = customtkinter.CTkButton(master=self.frame,
                                                text="messure weight",
                                                text_font=("Roboto Medium", 10),
                                                command=self.messure)
        self.messure_bttn.grid(row=9, column=0, pady=10, padx=20)

    def start_animate_fig(self):
        self.ani = FuncAnimation(self.graph.fig, self.graph.animate, interval=100)

    def remove_calc(self):
        self.scale_data.grid_remove()


    def messure(self):
        # returns the average of the last 5 sensor values
        arr =self.graph.data[-6:-1]
        print(arr)
        avg = np.average(arr)
        print(avg)
        self.calculation= str(avg) + " g"
        self.scale_data = customtkinter.CTkLabel(master=self.frame,
                                            text=self.calculation,
                                            text_font=("Roboto Medium", 16),
                                            pady= 5)
        self.scale_data.grid(row=1, column=0, pady=10, padx=10)
        self.scale_data.after(5000, self.remove_calc)


class App(customtkinter.CTk):
    WIDTH = 900
    HEIGHT = 650


    def __init__(self):
        super().__init__()

        self.title("Gutter Scale graph")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # ============ create three frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # main frame
        self.main_frame = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nswe")
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        self.side_bar = SideBar(self)
        self.calibrate_screen = CalibrateScreen(self.main_frame)
        self.weightgutter_screen = WeighGutterScreen(self.main_frame)

        self.side_bar.frame.grid(row=0, column=0, sticky="nswe")

    def change_page(self):
        print("Button pressed")
        print(self.side_bar.weigh_bttn.state)
        if self.side_bar.weigh_bttn.state == 'disabled':
            self.weightgutter_screen.frame.grid_remove()
            self.calibrate_screen.frame.grid()
            self.side_bar.weigh_bttn.configure(state='normal', text_font=("Roboto Medium", 10))
            self.side_bar.callibrate_bttn.configure(state='disabled', text_font=("Roboto Medium", 8))
        else:
            self.calibrate_screen.frame.grid_remove()
            self.weightgutter_screen.frame.grid()
            self.side_bar.callibrate_bttn.configure(state='normal', text_font=("Roboto Medium", 10))
            self.side_bar.weigh_bttn.configure(state='disabled', text_font=("Roboto Medium", 8))


    def on_closing(self, event=0):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
