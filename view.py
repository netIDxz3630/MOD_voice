import tkinter as Tk
from matplotlib import pyplot as plt
import numpy as np
from tkinter import filedialog as fd
from tkinter import messagebox

class View(Tk.Tk):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.config(padx=10, pady=6)
        self.resizable(False, False)

        self.running = True
        self.show_wave = False
        self.show_spectrum = False

        # Variables
        self.status = Tk.StringVar(value='Stopped')
        self.file_path = Tk.StringVar(value='')
        self.save_file = Tk.BooleanVar()
        self.save_name = Tk.StringVar(value='recording.wav')

        ##### IO Frame #####
        self.io_frame = Tk.LabelFrame(self, text="Input/Output Setting", padx=5, pady=5)
        self.io_frame.grid(row=0, column=0, columnspan=2)
        
        # IO Frame: 1st Line
        self.input_mode = Tk.IntVar(value=1)
        self.mic_btn = Tk.Radiobutton(
            self.io_frame,
            text="Microph",
            variable=self.input_mode,
            command=self.on_input_change,
            value=1,
        )
        self.mic_btn.grid(row=0, column=0, sticky='W', padx=4)

        self.file_btn = Tk.Radiobutton(
            self.io_frame,
            text="Wave File",
            variable=self.input_mode,
            command=self.on_input_change,
            value=2,
        )
        self.file_btn.grid(row=0, column=1, sticky='W', padx=5)

        Tk.Label(self.io_frame, text = 'Status:').grid(row=0, column=2, sticky='E')
        Tk.Label(
            self.io_frame,
            textvariable = self.status,
            width = 12,
            relief = Tk.SUNKEN,
            bd = 1
        ).grid(row=0, column=3, padx = 10, sticky='E')

        # IO Frame: 2ed Line
        self.open_btn = Tk.Button(
            self.io_frame,
            text = 'Open File',
            padx = 1,
            bd = 1,
            command = self.handle_open_file
        )
        self.open_btn.grid(row=1, column=0, pady=5)
        self.open_btn.configure(state='disable')

        io_label = Tk.Frame(self.io_frame, padx=10)
        io_label.grid(row=1, column=1, columnspan=3)
        Tk.Label(
            io_label,
            textvariable=self.file_path,
            width = 50,
            relief = Tk.SUNKEN,
            anchor='w',
            bd = 1
        ).pack()

        # IO Frame: 3rd Line
        self.save_btn = Tk.Checkbutton(
            self.io_frame,
            text = "Save File",
            variable = self.save_file,
            onvalue = True,
            offvalue = False
        )
        self.save_btn.grid(row=2, column=0)

        self.save_entry = Tk.Entry(
            self.io_frame,
            textvariable=self.save_name,
            width = 50,
            bd = 1
        )
        self.save_entry.grid(row=2, column=1, columnspan=3)

        # IO Frame: 4th Line
        Tk.Button(
            self.io_frame,
            text = 'Start',
            padx = 22,
            bd = 1,
            command = self.start_play
        ).grid(row=3, column=0, pady = 8)

        Tk.Button(
            self.io_frame,
            text = 'Stop',
            padx = 22,
            bd = 1,
            command = self.stop_play
        ).grid(row=3, column=1, pady = 8)


        ##### Effect Selector #####
        self.effect_selector = Tk.LabelFrame(self, text="Sound Effects", padx=8, pady=5)
        self.effect_selector.grid(row=1, column=0, pady=5, sticky='NW')
        
        self.echo_enable = Tk.BooleanVar()
        self.vibrato_enable = Tk.BooleanVar()
        self.modulation_enable = Tk.BooleanVar()

        Tk.Label(
            self.effect_selector,
            text = 'Enable',
            padx = 3,
            relief = Tk.SUNKEN,
            bd = 1
        ).grid(row=0, column=0, pady=5)

        Tk.Checkbutton(
            self.effect_selector,
            text = 'Echo',
            variable = self.echo_enable,
            onvalue = True,
            offvalue = False
        ).grid(row=1, column=0, sticky='W')

        Tk.Checkbutton(
            self.effect_selector,
            text = 'Vibrato',
            variable = self.vibrato_enable,
            onvalue = True,
            offvalue = False
        ).grid(row=2, column=0, sticky='W')

        Tk.Checkbutton(
            self.effect_selector,
            text = 'Modulation Frequency',
            variable = self.modulation_enable,
            onvalue = True,
            offvalue = False
        ).grid(row=3, column=0, sticky='W')

        ##### Options #####
        self.button_frame = Tk.LabelFrame(self, text="Options", padx=10, pady=5)
        self.button_frame.grid(row=2, column=0, columnspan=2, sticky='W')

        # Button - Wave Graph
        Tk.Button(
            self.button_frame,
            text = 'Wave Graph',
            padx = 10,
            bd = 1,
            command = self.open_wave
        ).grid(row=0, column=0)
    
        # Button - Spectrum Graph
        Tk.Button(
            self.button_frame,
            text = 'Spectrum Graph',
            padx = 10,
            bd = 1,
            command = self.open_spectrum
        ).grid(row=0, column=1, padx=20)

        # Button - Quit
        Tk.Button(
            self.button_frame,
            text = 'Quit',
            padx = 10,
            bd = 1,
            command = self.handle_quit
        ).grid(row=0, column=2)


        ##### Effect Frame #####
        self.effect_frame = Tk.LabelFrame(self, text="Effect Configure", padx=5)
        self.effect_frame.grid(row=1, column=1, sticky='NE', pady=5)

        # Effect Frame - mode select
        self.effect_radio = Tk.Frame(self.effect_frame)
        self.effect_radio.grid(row=0, column=0, sticky='W')

        self.effect_mode = Tk.IntVar(value=0)
        
        Tk.Radiobutton(
            self.effect_radio,
            text="Echo",
            variable=self.effect_mode,
            value=0,
            command=self.on_effect_mode_change
        ).grid(row=0, column=0, sticky='W', padx=4)

        Tk.Radiobutton(
            self.effect_radio,
            text="Vibrato",
            variable=self.effect_mode,
            value=1,
            command=self.on_effect_mode_change
        ).grid(row=0, column=1, sticky='W', padx=4)

        Tk.Radiobutton(
            self.effect_radio,
            text="Modulation change",
            variable=self.effect_mode,
            value=2,
            command=self.on_effect_mode_change
        ).grid(row=0, column=2, sticky='W', padx=4)

        ### Echo ###
        self.echo_frame = Tk.Frame(self.effect_frame, padx=5)
        self.echo_frame.grid(row=1, column=0, sticky='W')

        self.echo_feedback = Tk.DoubleVar(value = 70)
        self.echo_delay = Tk.DoubleVar(value = 0.1)

        # First line
        self.generate_slider(self.echo_frame, self.echo_feedback,
            0, 'Feedback (%)', 0.0, 100.0, 1.0)

        # Second line
        self.generate_slider(self.echo_frame, self.echo_delay,
            1, 'Delay (s)', 0.01, 0.50, 0.01)
        
        ### Modulation Frequency ###
        self.modulation_frame = Tk.Frame(self.effect_frame, padx=5)
        self.modulation_frame.grid(row=1, column=0, sticky='W')

        self.modulation_feedback = Tk.DoubleVar(value = 100)
        self.modulation_frequency = Tk.DoubleVar(value = 0.1)

        # First line
        self.generate_slider(self.modulation_frame, self.modulation_feedback,
            0, 'Feedback (%)', 0.0, 100.0, 1.0)

        # Second line
        self.generate_slider(self.modulation_frame, self.modulation_frequency,
            1, 'Frequency (Hz)', 0, 1000, 50)
        
        ### Vibrato ###
        self.vibrato_frame = Tk.Frame(self.effect_frame, padx=5)
        # self.vibrato_frame.grid(row=1, column=0, sticky='W')

        self.vibrato_f0 = Tk.DoubleVar(value = 10)
        self.vibrato_w = Tk.DoubleVar(value = 0.2)

        # First line
        self.generate_slider(self.vibrato_frame, self.vibrato_f0,
            0, 'Oscillation f0', 1.0, 20.0, 1.0)

        # Second line
        self.generate_slider(self.vibrato_frame, self.vibrato_w,
            1, 'Oscillation W', 0.1, 0.5, 0.1)
        
        self.frames = [self.echo_frame, self.vibrato_frame, self.modulation_frame]
        plt.ion()
    
    def handle_quit(self):
        self.running = False
    
    def is_running(self):
        return self.running

    def on_effect_mode_change(self):
        mode = self.effect_mode.get()
        for i, frame in enumerate(self.frames):
            if i == mode:
                frame.grid(row=1, column=0, sticky='W')
            else:
                frame.grid_remove()

    def on_input_change(self):
        mode = self.input_mode.get()
        if mode == 1:
            self.open_btn.configure(state='disable')
        if mode == 2:
            self.open_btn.configure(state='normal')

    def handle_open_file(self):
        filepath = fd.askopenfilename(filetypes=(('Wave File', '*.wav'),))
        if filepath:
            self.file_path.set(filepath)
            self.status.set('File Opened')

    def start_play(self):
        mode = self.input_mode.get()
        if mode == 1:
            self.status.set('Recording')
        elif mode == 2:
            if self.file_path.get():
                self.status.set('Playing')
            else:
                messagebox.showerror('Error', 'Please open a wave file')
                return
        self.mic_btn.configure(state='disable')
        self.file_btn.configure(state='disable')
        self.open_btn.configure(state='disable')
        self.save_btn.configure(state='disable')
        self.save_entry.configure(state='disable')
        self.app.change_mode(mode)

    def stop_play(self):
        if self.save_file.get():
            self.status.set('File Saved')
        else:
            self.status.set('Stopped')
        self.mic_btn.configure(state='normal')
        self.file_btn.configure(state='normal')
        self.open_btn.configure(state='normal')
        self.save_btn.configure(state='normal')
        self.save_entry.configure(state='normal')
        self.app.change_mode(0)
        self.app.stop_audio()

    def open_wave(self):
        plt.figure(1)

        plt.xlabel('Time (ms)')

        self.show_wave = True
        self.wave_x, = plt.plot([], [], color = 'blue', label='Original')
        self.wave_y, = plt.plot([], [], color = 'orange', label='Processed')

        t = [n*1000/float(self.app.rate) for n in range(self.app.block_len)]

        plt.xlim(0, 1000.0 * self.app.block_len/self.app.rate)         # set x-axis limits
        plt.xlabel('Time (msec)')

        plt.ylim(-8000, 8000)
        
        self.wave_x.set_xdata(t)
        self.wave_y.set_xdata(t)

        self.wave_x.set_ydata(np.zeros(self.app.block_len))
        self.wave_y.set_ydata(np.zeros(self.app.block_len))

        plt.legend()

    def open_spectrum(self):
        plt.figure(2)
        plt.xlim(0, 0.25 * self.app.rate)
        plt.ylim(0, 20 * self.app.rate)
        plt.xlabel('Frequency (Hz)')

        self.show_spectrum = True
        self.spectrum_x, = plt.plot([], [], color = 'blue', label='Original')
        self.spectrum_y, = plt.plot([], [], color = 'orange', label='Processed')

        f = self.app.rate / self.app.block_len * np.arange(0, self.app.block_len)
        
        self.spectrum_x.set_xdata(f)
        self.spectrum_y.set_xdata(f)

        self.spectrum_x.set_ydata(np.zeros(self.app.block_len))
        self.spectrum_y.set_ydata(np.zeros(self.app.block_len))

        plt.legend()
    
    def generate_slider(self, frame, slider_var, row, title, min_num, max_num, resolution):
        Tk.Label(
            frame,
            text = title,
            padx = 3,
            width = 11,
            anchor = 'e',
            bd = 1
        ).grid(row=row, column=0, sticky='E', pady=5)

        Tk.Label(
            frame,
            textvariable = slider_var,
            width = 5,
            relief = Tk.SUNKEN,
            bd = 1
        ).grid(row=row, column=1, padx=8)

        Tk.Label(
            frame,
            text = min_num,
            width = 4,
            padx = 3,
            bd = 1
        ).grid(row=row, column=2)

        Tk.Scale(
            frame,
            orient = 'horizontal',
            showvalue = False,
            variable = slider_var,
            sliderlength = 20,
            from_ = min_num,
            to = max_num,
            resolution = resolution,
            length = 120
        ).grid(row=row, column=3, padx=5)

        Tk.Label(
            frame,
            text = max_num,
            width = 4,
            padx = 3,
            bd = 1
        ).grid(row=row, column=4)