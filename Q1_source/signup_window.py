import tkinter as tk
from tkinter import ttk, Frame

class ISignupCallback:
    """
    Interface for handling signup callbacks, such as successfully signing up.
    """

    def on_signup(self):
        raise NotImplementedError

class SignupWindow(tk.Tk):
    """
    SignupWindow class provides a registration interface for users to create a new account. 
    It validates the uniqueness of usernames and ensures the password meets the length requirement.
    """

    def __init__(self, callback: ISignupCallback):
        """
        Initializes the SignupWindow and sets up the registration form.

        Args:
            callback (ISignupCallback): An object implementing the ISignupCallback interface 
            to handle the signup event.
        """
        super().__init__()

        self.title("Registration")
        self.__callback = callback
        '''(private) Callback object to handle the signup event.'''

        main_frame = tk.Frame(self, bg="#3F6BAA", height=150, width=250)
        main_frame.pack_propagate(0)  # Prevents resizing of the window to fit widgets
        main_frame = tk.Frame(self, bg="#3F6BAA", height=130, width=400)
        # pack_propagate prevents the window resizing to match the widgets
        main_frame.pack_propagate(0)

        main_frame.pack(fill="both", expand="true")

        self.geometry("626x500")
        self.resizable(0, 0)

        # Styles for labels and text
        text_styles = {"font": ("Verdana", 10), "background": "#3F6BAA", "foreground": "#E1FFFF"}
        
        # Entry fields for username and password
        self.__entry_user = ttk.Entry(main_frame, width=20, cursor="xterm")

        text_styles = {"font": ("Verdana", 10),
                       "background": "#3F6BAA",
                       "foreground": "#E1FFFF"}
        frame_signup = Frame(main_frame, bg="blue", relief="groove", bd=2)  # this is the frame that holds all the login details and buttons
        frame_signup.place(rely=0.30, relx=0.17, height=130, width=400)
        
        label_user = tk.Label(frame_signup, text_styles, text="New Username:")
        label_user.grid(row=1, column=0,padx=10, pady=20)

        label_pw = tk.Label(frame_signup, text_styles, text="New Password:")
        label_pw.grid(row=2, column=0, padx=5, pady=0)

        self.__entry_user = ttk.Entry(frame_signup, width=30, cursor="xterm")

        self.__entry_user.grid(row=1, column=1)

        self.__entry_pw = ttk.Entry(frame_signup, width=30, cursor="xterm", show="*")
        self.__entry_pw.grid(row=2, column=1)

        # Signup button to trigger the account creation process
        button = ttk.Button(frame_signup, text="Create Account", command=self.__signup)
        button.place(rely=0.70, relx=0.75)


    def __signup(self):
        """
        (private) Handles the signup process by validating user input and storing new credentials 
        if the username is unique and the password meets the required length.
        """
        user = self.__entry_user.get()
        pw = self.__entry_pw.get()

        # Validate the username's uniqueness
        if not self.__validate_user(user):
            tk.messagebox.showerror("Information", "That Username already exists")
        else:
            # Validate the password length
            if len(pw) > 3:
                with open("credentials.txt", "a") as credentials:
                    credentials.write(f"Username,{user},Password,{pw},\n")
                tk.messagebox.showinfo("Information", "Your account details have been stored.")
                self.destroy()
                self.__callback.on_signup()  # Trigger the callback after successful signup
            else:
                tk.messagebox.showerror("Information", "Your password needs to be longer than 3 values.")

    def __validate_user(self, username):
        """
        (private) Checks if the provided username is unique by verifying it against the existing 
        credentials in the text file.

        Args:
            username (str): The new username to validate.

        Returns:
            bool: True if the username is unique, False otherwise.
        """
        try:
            with open("credentials.txt", "r") as credentials:
                for line in credentials:
                    line = line.split(",")
                    if line[1] == username:
                        return False
            return True
        except FileNotFoundError:
            return True  # If no file exists, the username is valid (no users registered yet)
