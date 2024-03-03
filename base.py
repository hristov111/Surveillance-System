import threading
from tkinter import *
from tkinter import messagebox
import cv2 as cv
import time
from PIL import Image, ImageTk
import threading as t
import sqlite3
import bcrypt
import queue
import 

root = Tk()
root.title("Kali 1.0")
root.geometry("600x500")
root.resizable(False, False)
root.grid_columnconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)



class connect_database:
    def __init__(self):
        self.connection = sqlite3.connect("users.db")
        self.cursor = self.connection.cursor()

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                username text NOT NULL, 
                hashed_password BLOB NOT NULL
                )""")
        self.connection.commit()
        self.close_connection()

    def close_connection(self):
        self.connection.close()

    def create_user(self, username,password):
        self.connection = sqlite3.connect("users.db")
        self.cursor = self.connection.cursor()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.cursor.execute("INSERT INTO users (username ,hashed_password) VALUES (?, ? )", (username,hashed_password))
        # Insert the password and username into the database
        self.connection.commit()
        self.close_connection()
        messagebox.showinfo("Success", "user created successfully!")
    def update_password(self,username, new_password):
        self.connection = sqlite3.connect("users.db")
        self.cursor = self.connection.cursor()
        new_hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        # Insert the new password in the database
        self.cursor.execute("UPDATE users SET hashed_password =? WHERE username = ?", (new_hashed_password, username))
        messagebox.showinfo("Success", "password changed\nPlease login again to continue")
        self.connection.commit()
        self.close_connection()
    def delete_user(self,username,password):
        pass
    def check_user(self,username):
        self.connection = sqlite3.connect("users.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        result = self.cursor.fetchall()
        if result:
            self.close_connection()
            return False
        else:
            self.close_connection()
            return True
    def check_password(self,username):
        self.connection = sqlite3.connect("users.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT hashed_password FROM users WHERE username=?", (username,))
        res = self.cursor.fetchone()
        self.close_connection()
        return res[0] if res else None


class Main_Screen:
    def __init__(self,root):
        self.root = root
        self.root.config(background="black")
        self.current_password = None
        self.current_user = None
        self.main_label = Label(self.root, text="Welcome to Kali motion by Kalata", border=2, font=("Time New Roman", 20))
        self.main_label.grid(row=0,column=1,pady=15, columnspan=2)
        self.frame = LabelFrame(self.root, padx=50, pady=50, border=5)
        self.frame.grid(row=2, column=1, columnspan=2)
        self.username_label = Label(self.frame, text="Username:", border=2, font=("Times New Roman", 15))
        self.username_label.grid()
        self.user = StringVar()
        self.username_entry = Entry(self.frame, width=20, textvariable=self.user, border=5, font=('Helvetica', 15))
        self.username_entry.grid()
        # pass label
        self.password_label = Label(self.frame, text="Password:", border=2, font=("Times New Roman", 15))
        self.password_label.grid()
        # pass-typing
        self.password = StringVar()
        # pass entry
        self.password_entry = Entry(self.frame, width=20, textvariable=self.password, border=5, font=('Helvetica', 15))
        self.password_entry.grid()
        self.password_entry.bind("<Return>", lambda event: self.check_credentials())
        self.continue_butt = Button(self.frame, text="Continue", font=("Arial", 15), width=15, command=self.check_credentials)
        self.continue_butt.grid()
        self.exit_button = Button(self.root, text="EXIT", command=self.root.destroy, width=5, background='red', fg='black',
                             font=("Times New Roman", 15))
        self.exit_button.grid(row=4, column=0, padx=5, pady=5, sticky='sw')
        self.exit_button.bind("<Enter>", lambda e,user=self.exit_button:self.on_enter(e,user))
        self.exit_button.bind("<Leave>", lambda e,user=self.exit_button:self.on_leave(e,user))
        self.create_user_button = Button(self.root, text="Create an account", font=("Times New Roman", 15),width=20, background='red', fg='black',command=self.create_account)
        self.create_user_button.grid(row=1, column=1,pady=10, padx=5, sticky='se')
        self.create_user_button.bind("<Enter>", lambda e,user=self.create_user_button:self.on_enter(e,user))
        self.create_user_button.bind("<Leave>", lambda e,user=self.create_user_button:self.on_leave(e,user))
        self.password_correct = False
        self.confirmed_password = False
        self.confirmed_username = False
        self.database = connect_database()
    def create_account(self):
        account_window = Toplevel(self.root)
        account_window.title("Create account")
        account_window.geometry("500x500")
        self.create_user_button.config(state=DISABLED)
        self.username_entry.config(state=DISABLED)
        self.password_entry.config(state=DISABLED)
        self.continue_butt.config(state=DISABLED)
        account_window.resizable(False,False)
        username = StringVar()
        password = StringVar()
        confirm_password = StringVar()
        password.set("12345hello")
        confirm_password.set("12345hello")

        def onhover(e):
            submit_butt.config(fg='red')

        def outhover(e):
            submit_butt.config(fg='green')

        #     Create function for entry hovering
        def entry_onhover(e,entry):
            if entry.get() == "HeHeHohoHiHi":
                username_entry.delete(0, END)


        def password_onhover(e,entry):
            current = entry.get()
            if current == "12345hello":
                entry.delete(0, END)

        def check_password(e):
            current = password.get()
            self.password_correct = False
            is_lower = False
            is_upper = False
            is_number = False
            is_eight = False
            if len(current) == 8:
                eight_characters_label.config(text="✅ password must contain 8 characters")
                is_eight = True
            else:
                eight_characters_label.config(text="❌ password must contain 8 characters")
            for word in current:
                if word.islower():
                    is_lower = True
                elif word.isupper():
                    is_upper = True
                elif word.isdigit():
                    is_number = True
            if is_lower:
                one_lowercase_letter.config(text="✅ password must contain at least one lowercase letter")
            else:
                one_lowercase_letter.config(text="❌ password must contain at least one lowercase letter")
            if is_upper:
                one_uppercase_letter.config(text="✅ password must contain at least one uppercase letter")
            else:
                one_uppercase_letter.config(text="❌  password must contain at least one uppercase letter")
            if is_number:
                one_digit.config(text="✅ password must contain one digit")
            else:
                one_digit.config(text="❌ password must contain one digit")
            if is_lower and is_upper and is_number and is_eight:
                self.password_correct = True

        def check_confirmed_pass(e):
            self.confirmed_password = False
            if password.get() != confirm_password.get():
                confirmation_password_label.grid(row=6, column=1, sticky="W", pady=15)
                self.confirmed_password = False
            else:
                confirmation_password_label.grid_forget()
                self.confirmed_password = True

        def check_user_exists(e,entry):
            self.confirmed_username = False
            user,first_check,second_check,third_check,fourth_check = False,False,False,False,False
            username = entry.get()
            is_checked = self.database.check_user(username)
            if is_checked:
                user = True
                user_name_wrong.grid_forget()
            else:
                user_name_wrong.grid(row=3, column=1)
            if "$" in username or "@" in username or "_" in username:
                first_check = True
            for i in username:
                if i.isalpha():
                    second_check = True
                if i.isdigit():
                    third_check = True
            if len(username) < 11:
                fourth_check = True
            if first_check and second_check and third_check and fourth_check:
                username_check_characters.config(text="✅ Max. 10 characters allowed:$ @ _ a-z 1-9 ")
            else:
                username_check_characters.config(text="❌ Max. 10 characters allowed:$ @ _ a-z 1-9 ")
            if user and first_check and second_check and third_check and fourth_check:
                self.confirmed_username = True

        def wrap_up(pas,user):
            if self.password_correct and self.confirmed_password and self.confirmed_username:
                username = user.get()
                password = pas.get()
                self.database.create_user(username,password)
                self.create_user_button.config(state=ACTIVE)
                self.password_entry.config(state=NORMAL)
                self.username_entry.config(state=NORMAL)
                self.continue_butt.config(state=ACTIVE)
                account_window.destroy()
            else:
                messagebox.showerror("Error", "Please enter password and username")
        def close_window():
            account_window.destroy()
            self.create_user_button.config(state=ACTIVE)
            self.password_entry.config(state=NORMAL)
            self.username_entry.config(state=NORMAL)
            self.continue_butt.config(state=ACTIVE)


        user_name_label = Label(account_window, text="username: ", font=("Times New Roman", 15))
        user_name_label.grid(row=1, column=0, pady=15, sticky="W")
        username_entry = Entry(account_window, textvariable=username, font=("Times New Roman", 15), border=5,width=30)
        username_entry.bind("<Button-1>", lambda e, entry=username_entry:entry_onhover(e,entry))
        username_entry.bind("<KeyRelease>", lambda e, entry=username_entry:check_user_exists(e,username_entry))

        username_check_characters = Label(account_window, text="❌ Max. 10 characters allowed:$ @ _ a-z 1-9 ")
        username_check_characters.grid(row=2, column=1, sticky="W")
        username_entry.insert(0, "HeHeHohoHiHi")
        username_entry.grid(row=1, column=1)

        password_label = Label(account_window, text="password: ", font=("Times New Roman", 15))
        password_label.grid(row=4, column=0, sticky="W")
        password_entry = Entry(account_window, textvariable=password, font=("Times New Roman", 15), border=5,width=30)
        password_entry.bind("<Button-1>",  lambda e,entry=password_entry:password_onhover(e,entry))
        password_entry.bind("<KeyRelease>", check_password)
        password_entry.grid(row=4, column=1,pady=10)

        confirm_password_label = Label(account_window, text="confirm password: ", font=("Times New Roman", 15))
        confirm_password_label.grid(row=5, column=0, sticky="W")
        confirm_password_entry = Entry(account_window, textvariable=confirm_password, font=("Times New Roman", 15), border=5,width=30)
        confirm_password_entry.bind("<Button-1>", lambda e,entry=confirm_password_entry:password_onhover(e,entry))
        confirm_password_entry.grid(row=5, column=1, pady=5)
        confirm_password_entry.bind("<KeyRelease>" ,check_confirmed_pass)

        eight_characters_label = Label(account_window, text="❌ password must contain 8 characters")
        eight_characters_label.grid(row=7,column=1, sticky="W")
        one_uppercase_letter = Label(account_window, text="❌ password must contain at least one uppercase letter")
        one_uppercase_letter.grid(row=8,column=1,sticky="W")
        one_lowercase_letter = Label(account_window, text="❌ password must contain at least one lowercase letter")
        one_lowercase_letter.grid(row=9,column=1,sticky="W")
        one_digit = Label(account_window, text="❌ password must contain one digit")
        one_digit.grid(row=10, column=1, sticky="W")

        confirmation_password_label = Label(account_window, text="Password doesn't match", font=("Times New Roman", 15), background='red')
        # confirmation_password_label.grid(row=4, column=1, sticky="W", pady=15)
        confirmation_password_label.bind("<KeyRelease>", check_confirmed_pass)
        user_name_wrong = Label(account_window, text="Username is taken!",font=("Times New Roman", 15), background='red')

        submit_butt = Button(account_window, text="Save changes", font=("Times New Roman", 15), fg='green', command= lambda pass1=password_entry,user=username_entry:wrap_up(pass1,user))
        submit_butt.bind("<Enter>", onhover)
        submit_butt.bind("<Leave>", outhover)
        submit_butt.grid(row=11, column=0, columnspan=2, pady=15, padx=15, ipadx=20, ipady=10)

        account_window.protocol("WM_DELETE_WINDOW", close_window)
        account_window.mainloop()

    def check_credentials(self):
        hashed_pass = self.database.check_password(self.user.get())
        if hashed_pass and bcrypt.checkpw(self.password.get().encode('utf-8'), hashed_pass):
            self.current_user = self.user.get()
            self.current_password = self.password.get()
            self.create_user_button.config(state=DISABLED)
            self.password_entry.config(state=DISABLED)
            self.username_entry.config(state=DISABLED)
            self.continue_butt.config(state=DISABLED)
            start_secondary_widnow()
        else:
            self.popUp()
            self.password.set("")
            self.user.set("")

    def popUp(self):
        messagebox.showerror("Error", "username or password incorrect.Please try again")

    def on_enter(self,e,user):
        user.config(background='black', fg="red")

    def on_leave(self,e,user):
        user.config(background="red", fg='black')

main = Main_Screen(root)

def start_secondary_widnow():
    root2 = Toplevel(root)
    root2.configure(bg="black")
    root2.title("Camera configuration")
    root2.resizable(False, False)
    root2.geometry("640x480")
    secondary = Secondary_Page(root2)
    root2.protocol("WM_DELETE_WINDOW", secondary.close_window)
    root2.mainloop()

class Secondary_Page:
    def __init__(self,root2):
        self.root2 = root2
        self.root2.grid_rowconfigure(3, weight=1)  # Allocate extra space to the row with the scrolling canvas
        self.root2.grid_columnconfigure(0, weight=1)
        self.camera_entry_label = Label(root2, text="Enter the number of cameras:", font=("Times New Roman", 15), background="gray")
        self.camera_entry_label.grid(row=1, column=0,padx=5, pady=10)
        self.cameras_entry_var = IntVar()
        self.camera_button = None
        # Put these in a TOP canvas
        # ------------------------------------------
        canvas = Canvas(root2, width=600, height=50, bd=2, relief="ridge", bg="red")
        canvas.grid(row=0,column=0, columnspan=4, padx=10, pady=10)
        self.greet_user_label = Label(root2, text=f"Hello {self.resize_username(main.current_user)}", font=("Times New Roman", 15),fg="black",background="red")
        self.change_user_pass_butt = Button(root2, text="Change password", command=self.change_user_pass_page,
                                            font=("Times New Roman", 13), fg="red", background="black")
        self.change_user_pass_butt.bind("<Enter>", lambda e,butt=self.change_user_pass_butt: self.onhover(e,butt))
        self.change_user_pass_butt.bind("<Leave>", lambda e, butt=self.change_user_pass_butt:self.outhover(e,butt))
        canvas.create_window(80,30,window=self.greet_user_label)
        canvas.create_window(220,30, window=self.change_user_pass_butt)
        # --------------------------------------------------------------------------------------------
        self.clicked = 0
        self.label_array,self.camera_entries,self.entry_array,self.entry_vars = [],[],[],[]
        self.cameras_entry = Entry(root2, textvariable=self.cameras_entry_var, width=20, font=("Helvetica", 15))
        self.cameras_entry.grid(row=1, column=1, columnspan=2, padx=20)
        self.camera_entry_button = Button(root2, text="Submit", font=("Times New Roman", 15),
                                     command=self.create_indices,fg="red",background="black",border=5)
        self.camera_entry_button.bind("<Enter>", lambda e,butt=self.camera_entry_button:self.onhover(e,butt))
        self.camera_entry_button.bind("<Leave>", lambda e,butt=self.camera_entry_button:self.outhover(e,butt))
        self.camera_entry_button.grid(row=1, column=3, columnspan=2, padx=10, ipadx=10,ipady=10)
        self.camera_button = Button(root2)
        self.password_correct = False
        self.confirmed_password = False
        self.connected = False
        #Create the canvas for scrolling
        self.scrolling_canvas = Canvas(self.root2, bg='white', width=500, height = 300)
        self.scrollbar = Scrollbar(root2, orient='vertical', command=self.scrolling_canvas.yview)

        self.h_scrollbar = Scrollbar(self.root2, orient='horizontal', command=self.scrolling_canvas.xview)
        self.scrolling_canvas.configure(xscrollcommand=self.h_scrollbar.set)

        # Create a frame that will contain the widgets you want to scroll
        self.canvas_frame = Frame(self.scrolling_canvas, bg="red", border=5)
        self.scrolling_canvas.create_window((0, 0), window=self.canvas_frame, anchor='nw')

        # Set up the scrolling region based on the size of the content
        self.canvas_frame.bind("<Configure>", lambda e: self.scrolling_canvas.configure(
            scrollregion=self.scrolling_canvas.bbox("all")))

        # Grid or pack your scrollbar and canvas into the root2 window
        self.scrollbar.grid(row=3, column=3, sticky="ns")
        self.h_scrollbar.grid(row=4, column=0, columnspan=3, sticky="ew")
        self.scrolling_canvas.grid(row=3, column=0,columnspan=3)
        self.canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(0, weight=1)
        self.canvas_frame.bind("<MouseWheel>", self.on_mousewheel)
        self.scrolling_canvas.bind("<MouseWheel>", self.on_mousewheel)

        self.connect_button = Button(self.canvas_frame, text="Connect Now", font=("Times New Roman", 15), fg="red", background="black", command=self.connect)
        self.connect_button.bind("<Enter>", lambda e,butt=self.connect_button: self.onhover(e,butt))
        self.connect_button.bind("<Leave>", lambda e,butt=self.connect_button:self.outhover(e,butt))
        self.task_queue = queue.Queue()
        self.camera_list = []
        self.removable_labels = []
        self.frame_queues = {}
        self.windows = {}
        self.stop_event = threading.Event()
    def on_mousewheel(self, event):
        self.scrolling_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def onhover(self,e,button):
        button.config(fg='black', background='red')

    def outhover(self,e,button):
        button.config(fg='red', background='black')

    def resize_username(self,username):
        if len(username) > 7:
            username = username[:7]+"..."
            return username
        return username

    def change_user_pass_page(self):
        change = Toplevel(self.root2)
        change.title("Change Password and Username")
        change.resizable(False, False)
        change.geometry("500x350")
        new_password = StringVar()
        self.change_user_pass_butt.config(state=DISABLED)
        self.camera_entry_button.config(state=DISABLED)
        if self.camera_button is not None:
            self.camera_button.config(state=DISABLED)

        def close_window():
            change.destroy()
            self.change_user_pass_butt.config(state=ACTIVE)
            if not self.connected:
                self.camera_entry_button.config(state=ACTIVE)
                self.camera_button.config(state=ACTIVE)

        password = StringVar()
        confirm_password = StringVar()
        password.set("Example:12345hello")
        confirm_password.set("Example:12345hello")

        def onhover(e):
            submit_butt.config(fg='red')

        def outhover(e):
            submit_butt.config(fg='green')

        def password_onhover(e, entry):
            current = entry.get()
            if current == "Example:12345hello":
                entry.delete(0, END)

        def check_password(e):
            current = password.get()
            self.password_correct = False
            is_lower = False
            is_upper = False
            is_number = False
            is_eight = False
            if len(current) == 8:
                eight_characters_label.config(text="✅ password must contain 8 characters")
                is_eight = True
            else:
                eight_characters_label.config(text="❌ password must contain 8 characters")
            for word in current:
                if word.islower():
                    is_lower = True
                elif word.isupper():
                    is_upper = True
                elif word.isdigit():
                    is_number = True
            if is_lower:
                one_lowercase_letter.config(text="✅ password must contain at least one lowercase letter")
            else:
                one_lowercase_letter.config(text="❌ password must contain at least one lowercase letter")
            if is_upper:
                one_uppercase_letter.config(text="✅ password must contain at least one uppercase letter")
            else:
                one_uppercase_letter.config(text="❌  password must contain at least one uppercase letter")
            if is_number:
                one_digit.config(text="✅ password must contain one digit")
            else:
                one_digit.config(text="❌ password must contain one digit")
            if is_lower and is_upper and is_number and is_eight:
                self.password_correct = True

        def check_confirmed_pass(e):
            self.confirmed_password = False
            if password.get() != confirm_password.get():
                confirmation_password_label.grid(row=6, column=1, sticky="W", pady=15)
                self.confirmed_password = False
            else:
                confirmation_password_label.grid_forget()
                self.confirmed_password = True
        def wrap_up(username,pass1):
            if self.password_correct and self.confirmed_password:
                password = pass1.get()
                change.destroy()
                self.root2.destroy()
                main.database.update_password(username, password)
                main.create_user_button.config(state=ACTIVE)
                main.password_entry.config(state=NORMAL)
                main.username_entry.config(state=NORMAL)
                main.continue_butt.config(state=ACTIVE)
                main.password.set("")
                main.user.set("")
            else:
                messagebox.showerror("Error", "Please enter valid password")

        password_label = Label(change, text="password: ", font=("Times New Roman", 15))
        password_label.grid(row=4, column=0, sticky="W")
        password_entry = Entry(change, textvariable=password, font=("Times New Roman", 15), border=5, width=30)
        password_entry.bind("<Button-1>", lambda e, entry=password_entry: password_onhover(e, entry))
        password_entry.bind("<KeyRelease>", check_password)
        password_entry.grid(row=4, column=1, pady=10)

        confirm_password_label = Label(change, text="confirm password: ", font=("Times New Roman", 15))
        confirm_password_label.grid(row=5, column=0, sticky="W")
        confirm_password_entry = Entry(change, textvariable=confirm_password, font=("Times New Roman", 15),
                                       border=5, width=30)
        confirm_password_entry.bind("<Button-1>", lambda e, entry=confirm_password_entry: password_onhover(e, entry))
        confirm_password_entry.grid(row=5, column=1, pady=5)
        confirm_password_entry.bind("<KeyRelease>", check_confirmed_pass)

        eight_characters_label = Label(change, text="❌ password must contain 8 characters")
        eight_characters_label.grid(row=7, column=1, sticky="W")
        one_uppercase_letter = Label(change, text="❌ password must contain at least one uppercase letter")
        one_uppercase_letter.grid(row=8, column=1, sticky="W")
        one_lowercase_letter = Label(change, text="❌ password must contain at least one lowercase letter")
        one_lowercase_letter.grid(row=9, column=1, sticky="W")
        one_digit = Label(change, text="❌ password must contain one digit")
        one_digit.grid(row=10, column=1, sticky="W")

        confirmation_password_label = Label(change, text="Password doesn't match", font=("Times New Roman", 15),
                                            background='red')
        # confirmation_password_label.grid(row=4, column=1, sticky="W", pady=15)
        confirmation_password_label.bind("<KeyRelease>", check_confirmed_pass)
        submit_butt = Button(change, text="Save changes", font=("Times New Roman", 15), fg='green',
                             command=lambda pass1=password_entry: wrap_up(main.current_user, pass1))
        submit_butt.bind("<Enter>", onhover)
        submit_butt.bind("<Leave>", outhover)
        submit_butt.grid(row=11, column=0, columnspan=2, pady=15, padx=15, ipadx=20, ipady=10)




        change.protocol("WM_DELETE_WINDOW", close_window)
        change.mainloop()

    def create_indices(self):
        try:
            if self.cameras_entry_var.get() >5:
                messagebox.showerror("Error", "The maximum number of cameras is 5")
                self.cameras_entry_var.set(0)
                return
        except TclError:
            messagebox.showerror("Error", "Enter a number please")
            return
        self.entry_vars = []
        if self.clicked > 0:
            current = self.camera_entries[0]
            for i in range(current):
                self.label_array[i].destroy()
                self.entry_array[i].destroy()
            self.camera_entries.clear()
            self.label_array.clear()
            self.entry_array.clear()
        self.clicked += 1
        self.camera_entries.append(self.cameras_entry_var.get())
        row_counter = 0
        for i in range(self.cameras_entry_var.get()):
            label = Label(self.canvas_frame, text="Index:", font=("Times New Roman", 15), fg="gray")
            label.grid(row=row_counter, column=0, pady=5)
            index = IntVar()
            row_counter+=1
            entry = Entry(self.canvas_frame, textvariable=index, font=("Times New Roman", 15))
            entry.grid(row=row_counter, column=0, pady=5)
            row_counter+=1
            self.entry_vars.append(index)
            self.label_array.append(label)
            self.entry_array.append(entry)
        if self.cameras_entry_var.get() == 0:
            messagebox.showerror("Error", "Please select the number of cameras")
        if self.camera_button is not None:
            self.camera_button.destroy()
        if self.cameras_entry_var.get() != 0:

            self.camera_button = Button(self.canvas_frame, text="Check",
                               font=("Times New Roman", 15), command=lambda : self.check_for_indices(self.entry_vars),fg="red",background="black",border=5)
            self.camera_button.bind("<Enter>", lambda e,butt=self.camera_button:self.onhover(e,butt))
            self.camera_button.bind("<Leave>",lambda e,butt=self.camera_button:self.outhover(e,butt))
            self.camera_button.grid(row=row_counter+1,column=0,ipadx=10,ipady=10,pady=10)
            self.canvas_frame.update_idletasks()
            self.scrolling_canvas.configure(scrollregion=self.scrolling_canvas.bbox('all'))

    def check_for_indices(self,lists):
        try:
            list_set = [var for var in lists if var.get() == ""]
        except Exception:
            messagebox.showerror("Error", "Please enter a valid index")
            return
        set_list = set([var.get() for var  in lists])
        if len(set_list) != len(lists):
            messagebox.showerror("Error", "Please enter a non similar indices")
            return
        def check_camera(index_var,row):
            index = index_var.get()
            cap = cv.VideoCapture(index)
            if not cap.isOpened():
                self.root2.after(3000,lambda:self.update_label_failure(row,index))
                cap.release()
            else:
                self.camera_list.append(index)
                self.root2.after(2000,lambda:self.update_label_success(row,index))
                cap.release()
        def check_threads():
            alive = all(not t.is_alive() for t in threads)
            if alive:
                self.connect_button.grid(row=len(lists) + 1, column=1, padx=10)
                self.connected = True
            else:
                self.root2.after(100, check_threads)

        threads = []
        for i, index_var in enumerate(lists):
            label = Label(self.canvas_frame, text="⚠️ Checking please wait...", font=("Times New Roman", 15))
            label.grid(row=i, column=1, columnspan=2, padx=20)
            self.removable_labels.append(label)
            thread = t.Thread(target=check_camera, args=(index_var, i))
            threads.append(thread)
            thread.start()
        check_threads()
        self.camera_button['state'] = DISABLED
        self.camera_entry_button['state'] = DISABLED
    def update_label_success(self,row, index):
        label = Label(self.canvas_frame, text=f"✅ Camera with index {index} is accessible!",
                      font=("Times New Roman", 15))
        label.grid(row=row, column=1, columnspan=2, padx=20)
        self.removable_labels.append(label)


    def update_label_failure(self,row,index):
        label = Label(self.canvas_frame, text=f"❌ Camera with index {index} failed!", font=("Times New Roman", 15))
        label.grid(row=row, column=1, columnspan=2, padx=20)
        self.removable_labels.append(label)

    def connect(self):
        answer = messagebox.askyesno("Attention", f"Are you sure you want to connect to cameras with indices {",".join(str(x) for x in self.camera_list)}?")
        if answer:
            self.connect_button.config(state=DISABLED)
            self.start_cameras(self.camera_list)
        else:
            self.connected = False
            self.camera_button.configure(state=NORMAL,fg='red', background='black')
            self.camera_entry_button.configure(state=NORMAL, fg='red', background='black')
            self.connect_button.grid_forget()
            self.camera_list.clear()
            for label in self.removable_labels:
                label.grid_forget()

    def close_window(self):
        self.root2.destroy()
        main.create_user_button.config(state=ACTIVE)
        main.continue_butt.config(state=ACTIVE)
        main.password_entry.config(state=NORMAL)
        main.username_entry.config(state=NORMAL)
    def start_cameras(self,camera_list):
        self.stop_event = threading.Event()
        self.frame_queues = {}
        self.windows = {}
        for i in camera_list:
            self.frame_queues[i] = queue.Queue()
            # camera
            camera = Toplevel(self.root2)
            camera.title(f"Camera {i}")
            camera.geometry("640x1000")
            camera.resizable(False, False)
            #
            label = Label(camera, text="Hello Idiots")
            label.grid(row=1, column=0)
            self.windows[i] = camera
            camera.protocol("WM_DELETE_WINDOW",lambda window=camera:self.stop_cameras(window,self.stop_event))
            threading.Thread(target=self.grab_frames, args=(i,self.stop_event,self.frame_queues[i])).start()
            self.update_gui(i)




    def stop_cameras(self,win,stop):
        stop.set()
        win.destroy()
        self.connected = False
        self.camera_button.configure(state=NORMAL, fg='red', background='black')
        self.camera_entry_button.configure(state=NORMAL, fg='red', background='black')
        self.connect_button.grid_forget()
        self.connect_button.configure(state=NORMAL, fg='red', background='black')
        self.camera_list.clear()
        for label in self.removable_labels:
            label.grid_forget()
    def grab_frames(self,index,stop_event,frame_queue):
        cap = cv.VideoCapture(index)
        while not stop_event.is_set():
            ret, frame = cap.read()
            if ret:
                image = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)
                frame_queue.put(image)
        cap.release()
    def update_gui(self,i):
        window = self.windows[i]
        frame_queue = self.frame_queues[i]
        try:
            image = frame_queue.get()
            image = Image.fromarray(image)
            imgtk = ImageTk.PhotoImage(image=image)
            frame_label = Label(window, image=imgtk)
            frame_label.image = imgtk
            frame_label.grid(row=0, column=0)
        except queue.Empty:
            pass
        finally:
            window.after(20, lambda: self.update_gui(i))

root.mainloop()