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



class App(customtkinter.CTk):

    WIDTH = 900
    HEIGHT = 600

    def __init__(self):
        super().__init__()

        self.title("Gutter Scale graph")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed


        # ============ create three frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self, width=180, corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        # main frame
        self.main_frame = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nswe")
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        #  page 1 gutter scale
        self.calibration_frame = customtkinter.CTkFrame(master=self.main_frame, fg_color='grey', corner_radius=0)
        self.calibration_frame.grid(row=0, column=1, sticky="nswe")
        #  page 2 callibration
        self.scale_frame = customtkinter.CTkFrame(master= self.main_frame, fg_color='grey', corner_radius=0)
        self.scale_frame.grid(row=0, column=1, sticky="nswe")



        # ========= create figure=====
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        #=== array for serial data from scale
        self.data = np.array([])
        self.ani =FuncAnimation(self.fig, self.animate, interval=100)



        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.leftF_label = customtkinter.CTkLabel(master=self.frame_left,
                                                  text="Scale graphs",
                                                  text_font=("Roboto Medium", -16))  # font name and size in px
        self.leftF_label.grid(row=1, column=0, pady=10, padx=10)

        self.weigh_bttn = customtkinter.CTkButton(master=self.frame_left,
                                                  text="weigh gutter",
                                                  state="disabled",
                                                  text_font=("Roboto Medium",8),
                                                  command=self.button_event)
        self.weigh_bttn.grid(row=2, column=0, pady=10, padx=20)

        self.callibrate_bttn = customtkinter.CTkButton(master=self.frame_left,
                                                       text="Callibrate",
                                                       state='normal',
                                                       text_font=("Roboto Medium",10),
                                                       command=self.button_event)
        self.callibrate_bttn.grid(row=3, column=0, pady=10, padx=20)

        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Appearance Mode:", text_font=("", 9))
        self.label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=["Light", "Dark", "System"],
                                                        command=self.change_appearance_mode)
        self.optionmenu_1.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        #     ======== scale frame ========


        #     tare button
        self.messure_bttn = customtkinter.CTkButton(master=self.scale_frame,
                                                text="messure weight",
                                                text_font=("Roboto Medium", 10),
                                                command=self.messure)
        self.messure_bttn.grid(row=9, column=0, pady=10, padx=20)

        # ===== display figure =====
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.scale_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, pady=40, padx=40)

        #self.ani = FuncAnimation(self.fig, self.animate, interval=100)


    #     ==== start serial port
    #     self.data = np.array([])
    #     self.scale_frame.after(1, self.plot_data())
        # self.ser = sr.Serial('/dev/serial0', 9600, timeout=1)
        # self.ser.reset_input_buffer()

    # -----plot data-----
    def animate(self):
        global cond, data

        a = random.randint(500, 5000)

        self.ax.cla()
        self.ax.set_xticks([])
        self.ax.set_title('gutter scale')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('weight(g)')
        self.ax.set_ylim(-0.5, 5000)
        self.ax.set_yticks([0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000])

        if (len(data) < 100):
            self.data = np.append(data, a)
            print(data)
        else:
            data[0:99] = data[1:100]
            data[99] = a
        self.ax.plot(np.arange(0, len(data)), data)





    def button_event(self):
        print("Button pressed")
        print(self.weigh_bttn.state)
        if self.weigh_bttn.state == 'disabled':
            self.scale_frame.grid_remove()
            self.calibration_frame.grid()
            self.weigh_bttn.configure(state='normal', text_font=("Roboto Medium", 10))
            self.callibrate_bttn.configure(state='disabled', text_font=("Roboto Medium", 8))
        else:
            self.calibration_frame.grid_remove()
            self.scale_frame.grid()
            self.callibrate_bttn.configure(state='normal', text_font=("Roboto Medium", 10))
            self.weigh_bttn.configure(state='disabled', text_font=("Roboto Medium", 8))

    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self, event=0):
        self.destroy()

    def messure(self):
        print("messuring")







if __name__ == "__main__":
    app = App()
    app.mainloop()