from tkinter import Frame

class BasePage(Frame):
    def __init__(self, master, controller):
        super().__init__(master)

        self._controller = controller

        # Get screen width and height
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        # Set the main_frame to fill the screen
        self.main_frame = Frame(self, bg="#FFFFFF", height=screen_height, width=screen_width)
        self.main_frame.pack(fill="both", expand=True)  # Ensure it expands to fill the entire screen

        # self.main_frame.pack_propagate(0)
        self.main_frame.pack(fill="both", expand="true")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)