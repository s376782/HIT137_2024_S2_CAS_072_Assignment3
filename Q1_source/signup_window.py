import tkinter as tk
from tkinter import ttk

class ISignupCallback:
    def on_signup(self):
        raise NotImplementedError

class SignupWindow(tk.Tk):
    def __init__(self, callback: ISignupCallback):
        super().__init__()
        self.title("Registration")

        self.__callback = callback

        main_frame = tk.Frame(self, bg="#3F6BAA", height=150, width=250)
        # pack_propagate prevents the window resizing to match the widgets
        main_frame.pack_propagate(0)
        main_frame.pack(fill="both", expand="true")

        self.geometry("250x150")
        self.resizable(0, 0)

        text_styles = {"font": ("Verdana", 10),
                       "background": "#3F6BAA",
                       "foreground": "#E1FFFF"}

        label_user = tk.Label(main_frame, text_styles, text="New Username:")
        label_user.grid(row=1, column=0)

        label_pw = tk.Label(main_frame, text_styles, text="New Password:")
        label_pw.grid(row=2, column=0)

        self.__entry_user = ttk.Entry(main_frame, width=20, cursor="xterm")
        self.__entry_user.grid(row=1, column=1)

        self.__entry_pw = ttk.Entry(main_frame, width=20, cursor="xterm", show="*")
        self.__entry_pw.grid(row=2, column=1)

        button = ttk.Button(main_frame, text="Create Account", command=self.__signup)
        button.grid(row=4, column=1)

    def __signup(self):
        # Creates a text file with the Username and password
        user = self.__entry_user.get()
        pw = self.__entry_pw.get()
        validation = self.validate_user(user)
        if not validation:
            tk.messagebox.showerror("Information", "That Username already exists")
        else:
            if len(pw) > 3:
                credentials = open("credentials.txt", "a")
                credentials.write(f"Username,{user},Password,{pw},\n")
                credentials.close()
                tk.messagebox.showinfo("Information", "Your account details have been stored.")
                self.destroy()
                self.__callback.on_signup()
            else:
                tk.messagebox.showerror("Information", "Your password needs to be longer than 3 values.")

    def validate_user(self, username):
        # Checks the text file for a username/password combination.
        try:
            with open("credentials.txt", "r") as credentials:
                for line in credentials:
                    line = line.split(",")
                    if line[1] == username:
                        return False
            return True
        except FileNotFoundError:
            return True