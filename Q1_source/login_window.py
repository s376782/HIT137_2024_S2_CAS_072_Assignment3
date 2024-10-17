from tkinter import Tk, Frame, Label, messagebox, ttk

class ILoginCallback:
    """
    Interface to handle login callbacks such as login success and opening the signup window.
    """

    def on_login_success(self, username: str):
        raise NotImplementedError

    def on_open_signup(self):
        raise NotImplementedError

class LoginWindow(Tk):
    """
    LoginWindow class creates a simple login interface where users can enter their credentials 
    to log in or navigate to a signup page.
    """

    def __init__(self, callback: ILoginCallback):
        """
        Initializes the LoginWindow and sets up the UI components for user input.

        Args:
            callback (ILoginCallback): An object implementing the ILoginCallback interface 
            to handle login events.
        """
        super().__init__()

        self.__callback = callback
        '''(private) Callback object to handle login-related events.'''

        # Main Frame setup
        main_frame = Frame(self, bg="#708090") #, height=431, width=626)
        main_frame.pack(fill='both', expand=True)
        
        self.geometry("626x500")  # Set window size
        self.resizable(0, 0)  # Prevent resizing

        # Style for labels and text
        title_styles = {"font": ("Trebuchet MS Bold", 16), "background": "blue"}
        text_styles = {"font": ("Verdana", 14), "background": "blue", "foreground": "#E1FFFF"}

        # Login Frame
        frame_login = Frame(main_frame, bg="blue", relief="groove", bd=2)  # this is the frame that holds all the login details and buttons
        frame_login.place(rely=0.30, relx=0.17, height=130, width=400)

        # Labels
        label_title = Label(frame_login, title_styles, text="Login")
        label_title.grid(row=0, column=0, columnspan=1)

        label_user = Label(frame_login, text_styles, text="Username:")
        label_user.grid(row=1, column=0)

        label_pw = Label(frame_login, text_styles, text="Password:")
        label_pw.grid(row=2, column=0)

        # Entry fields
        self.__entry_user = ttk.Entry(frame_login, width=45, cursor="xterm")
        self.__entry_user.grid(row=1, column=1)

        self.__entry_pw = ttk.Entry(frame_login, width=45, cursor="xterm", show="*")
        self.__entry_pw.grid(row=2, column=1)

        # Buttons
        button = ttk.Button(frame_login, text="Login", command=self.__login)
        button.place(rely=0.70, relx=0.50)

        signup_btn = ttk.Button(frame_login, text="Register", command=self.__signup)
        signup_btn.place(rely=0.70, relx=0.75)

    def __signup(self):
        """
        (private) Triggers the signup event via the callback.
        """
        self.__callback.on_open_signup()    

    def __login(self):
        """
        (private) Handles the login process, validates user input, and triggers appropriate actions 
        if login is successful or fails.
        """
        username = self.__entry_user.get()
        password = self.__entry_pw.get()

        # Validate username and password
        validation = self.__validate(username, password)
        if validation:
            messagebox.showinfo("Login Successful", f'Welcome {username}')
            self.__callback.on_login_success(username)
        else:
            messagebox.showerror("Login Failed", "The Username or Password you have entered are incorrect ")

    def __validate(self, username, password):
        """
        (private) Validates the provided username and password by checking them against a stored file.

        Args:
            username (str): The username provided by the user.
            password (str): The password provided by the user.

        Returns:
            bool: True if the credentials are valid, False otherwise.
        """
        try:
            with open("credentials.txt", "r") as credentials:
                for line in credentials:
                    line = line.split(",")
                    if line[1] == username and line[3] == password:
                        return True
                return False
        except FileNotFoundError:
            messagebox.showerror("Error", "No credentials file found. Please register first.")
            return False