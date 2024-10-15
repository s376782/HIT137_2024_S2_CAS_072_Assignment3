from tkinter import Frame, Label, messagebox, ttk
from tkinter.simpledialog import Dialog
from typing import override

class ILoginCallback:
    def onLoginSuccess(self, username: str):
        raise NotImplementedError

    def onSignup(self):
        raise NotImplementedError

    def onCancel(self):
        raise NotImplementedError

class LoginDialog(Dialog):
    def __init__(self, parent, callback: ILoginCallback, title = None):
        super().__init__(parent, title)
        self.callback = callback
        self.cancel = True

    @override
    def body(self, master: Frame):
        main_frame = Frame(master, bg="#708090", height=431, width=626)
        main_frame.pack(fill='both', expand=True)
        
        self.geometry("626x500")  # Sets window size to 626w x 431h pixels
        self.resizable(0, 0)  # This prevents any resizing of the screen
        title_styles = {"font": ("Trebuchet MS Bold", 16), "background": "blue"}

        text_styles = {"font": ("Verdana", 14),
                       "background": "blue",
                       "foreground": "#E1FFFF"}

        frame_login = Frame(main_frame, bg="blue", relief="groove", bd=2)  # this is the frame that holds all the login details and buttons
        frame_login.place(rely=0.30, relx=0.17, height=130, width=400)

        label_title = Label(frame_login, title_styles, text="Login")
        label_title.grid(row=0, column=1, columnspan=1)

        label_user = Label(frame_login, text_styles, text="Username:")
        label_user.grid(row=1, column=0)

        label_pw = Label(frame_login, text_styles, text="Password:")
        label_pw.grid(row=2, column=0)

        self.entry_user = ttk.Entry(frame_login, width=45, cursor="xterm")
        self.entry_user.grid(row=1, column=1)

        self.entry_pw = ttk.Entry(frame_login, width=45, cursor="xterm", show="*")
        self.entry_pw.grid(row=2, column=1)

        button = ttk.Button(frame_login, text="Login", command=lambda: self.login)
        button.place(rely=0.70, relx=0.50)

        signup_btn = ttk.Button(frame_login, text="Register", command=lambda: self.callback.onSignup)
        signup_btn.place(rely=0.70, relx=0.75)

    @override
    def buttonbox(self):
        pass # override to remove the standard buttons

    @override
    def destroy(self):
        super().destroy()
        if self.cancel:
            self.callback.onCancel()

    def signup(self):
        self.cancel = False
        self.callback.onSignup()    

    def login(self):
        username = self.entry_user.get()
        password = self.entry_pw.get()

        # if your want to run the script as it is set validation = True
        validation = self.validate(username, password)
        if validation:
            messagebox.showinfo("Login Successful", f'Welcome {username}')
            self.cancel = False
            self.callback.onLoginSuccess(username)
        else:
            messagebox.showerror("Information", "The Username or Password you have entered are incorrect ")

    def validate(username, password):
        # Checks the text file for a username/password combination.
        try:
            with open("credentials.txt", "r") as credentials:
                for line in credentials:
                    line = line.split(",")
                    if line[1] == username and line[3] == password:
                        return True
                return False
        except FileNotFoundError:
            print("You need to Register first or amend Line 71 to if True:")
            return False