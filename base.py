import cv2
import cv2 as cv
import threading as tr
import sqlite3
import bcrypt
import threading
import time
import os
from datetime import datetime
from collections import deque
from tkinter import *
from tkinter import messagebox
import shutil
import queue
import numpy as np
from threading import Timer
from PIL import Image, ImageTk
import pdb


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
        self.main_label = Label(self.root, text="Welcome to Kala Motion", border=2, font=("Time New Roman", 20),fg="red", background='black')
        self.main_label.grid(row=0,column=1,pady=15,columnspan=2,padx=60)
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
global secondary

def start_secondary_widnow():
    global secondary
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
        # self.change_user_pass_butt.bind("<Enter>", lambda e,butt=self.change_user_pass_butt: self.onhover(e,butt))
        # self.change_user_pass_butt.bind("<Leave>", lambda e, butt=self.change_user_pass_butt:self.outhover(e,butt))
        self.search_button = Button(root2, text="Search files", font=("Times New Roman", 13), fg="red", background="black", command=lambda :search_start(root2))
        self.search_button.bind("<Enter>", lambda e,butt=self.search_button:self.onhover(e,butt))
        self.search_button.bind("<Leave>", lambda e,butt=self.search_button:self.outhover(e,butt))
        canvas.create_window(350, 30, window=self.search_button)
        canvas.create_window(80,30,window=self.greet_user_label)
        canvas.create_window(220,30, window=self.change_user_pass_butt)
        # --------------------------------------------------------------------------------------------
        self.clicked = 0
        self.label_array,self.camera_entries,self.entry_array,self.entry_vars = [],[],[],[]
        self.cameras_entry = Entry(root2, textvariable=self.cameras_entry_var, width=20, font=("Helvetica", 15))
        self.cameras_entry.grid(row=1, column=1, columnspan=2, padx=20)
        self.camera_entry_button = Button(root2, text="Submit", font=("Times New Roman", 15),
                                     command=self.create_indices,fg="red",background="black",border=5)
        # self.camera_entry_button.bind("<Enter>", lambda e,butt=self.camera_entry_button:self.onhover(e,butt))
        # self.camera_entry_button.bind("<Leave>", lambda e,butt=self.camera_entry_button:self.outhover(e,butt))
        self.camera_entry_button.grid(row=1, column=3, columnspan=2, padx=10, ipadx=10,ipady=10)
        self.camera_button = Button(root2)
        self.password_correct = False
        self.confirmed_password = False
        self.connected = False
        #Create the canvas for scrolling
        self.scrolling_canvas = Canvas(self.root2, bg='white', width=500, height = 300, background='red')
        self.scrollbar = Scrollbar(root2, orient=VERTICAL, command=self.scrolling_canvas.yview)

        self.h_scrollbar = Scrollbar(self.root2, orient=HORIZONTAL, command=self.scrolling_canvas.xview)
        self.scrolling_canvas.configure(xscrollcommand=self.h_scrollbar.set)
        self.scrolling_canvas.configure(yscrollcommand=self.scrollbar.set)

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
        # self.connect_button.bind("<Enter>", lambda e,butt=self.connect_button: self.onhover(e,butt))
        # self.connect_button.bind("<Leave>", lambda e,butt=self.connect_button:self.outhover(e,butt))
        self.task_queue = queue.Queue()
        self.camera_list = []
        self.removable_labels = []
        self.success = False
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
            # self.camera_button.bind("<Enter>", lambda e,butt=self.camera_button:self.onhover(e,butt))
            # self.camera_button.bind("<Leave>",lambda e,butt=self.camera_button:self.outhover(e,butt))
            self.camera_button.grid(row=row_counter+1,column=0,ipadx=10,ipady=10,pady=10)
            self.canvas_frame.update_idletasks()
            self.scrolling_canvas.configure(scrollregion=self.scrolling_canvas.bbox('all'))

    def check_for_indices(self,lists):
        for label in self.removable_labels:
            label.grid_forget()
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
                self.root2.after(3000, lambda :self.update_label_failure(row,index))
                cap.release()
            else:
                self.camera_list.append(index)
                self.root2.after(2000,lambda: self.update_label_success(row,index))
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
            thread = tr.Thread(target=check_camera, args=(index_var, i))
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
            if len(self.camera_list) != 0:
                start_cameras(self.root2)
                self.connect_button.config(state=DISABLED)
            else:
                messagebox.showerror("Error", "INDEX DOESNT EXIST")
                self.connected = False
                self.camera_button.configure(state=NORMAL, fg='red', background='black')
                self.camera_entry_button.configure(state=NORMAL, fg='red', background='black')
                self.connect_button.grid_forget()
                for label in self.removable_labels:
                    label.grid_forget()
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

def search_start(main_windwo):
    search_win = Toplevel(main_windwo)
    search_win.title("Search Engine")
    search_win.geometry("700x600")
    search_win.resizable(False, False)
    search = Seach_Engine_Window(search_win)
    search_win.protocol("WM_DELETE_WINDOW", search.close)
    search_win.resizable(False, False)
    search_win.mainloop()
class Seach_Engine_Window:
    def __init__(self,main_root):
        self.main_root = main_root

        # Create a top frame for fixed-position widgets
        self.top_frame = Frame(self.main_root)
        self.top_frame.grid(row=0,column=0)

        # Main frame for scrollable content

        self.scrolling_canvas = Canvas(self.main_root, bg='white', width=646, height=550, background='white')
        self.scrollbar = Scrollbar(self.main_root, orient=VERTICAL, command=self.scrolling_canvas.yview)

        self.scrolling_canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a frame that will contain the widgets you want to scroll
        self.canvas_frame = Frame(self.scrolling_canvas, border=5)
        self.scrolling_canvas.create_window((0, 0), window=self.canvas_frame, anchor='nw')

        # Set up the scrolling region based on the size of the content
        self.canvas_frame.bind("<Configure>", lambda e: self.scrolling_canvas.configure(
            scrollregion=self.scrolling_canvas.bbox("all")))

        # Grid or pack your scrollbar and canvas into the root2 window
        self.scrollbar.grid(row=1, column=3, sticky="ns")
        self.scrolling_canvas.grid(row=1, column=0, columnspan=2)
        self.canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(0, weight=1)
        self.canvas_frame.bind("<MouseWheel>", self.on_mousewheel)
        self.scrolling_canvas.bind("<MouseWheel>", self.on_mousewheel)


        # Place the OptionMenu and Entry in the top frame so they don't move
        self.options = ["Videos", "Photos"]
        self.option = StringVar()
        self.option.set(self.options[0])
        self.drop_down = OptionMenu(self.top_frame, self.option, *self.options)
        self.drop_down.pack(side=LEFT)

        self.search_text = StringVar()

        self.main_entr = Entry(self.top_frame, textvariable=self.search_text, width=40, font=("Times New Roman", 20),border=5)
        self.main_entr.insert(0, "Example: 02-27-2024_18-11-34")
        self.main_entr.pack(side=TOP)
        self.main_entr.bind("<Button-1>",lambda e: self.entry_onhover(e))
        self.main_entr.bind("<KeyRelease>", lambda e: self.start_checking(e))


        self.current_month = None
        self.current_day = None
        self.current_year = None
        self.labels = []
        self.buttons = []
        self.typed = 0
        self.timer = None
        self.sorted_by_mtime = []
        self.parent_dir = "C:\\Users\\haram\\PycharmProjects\\motionDetection\\videos"
        self.first_search = []
        self.second_searh = []
        self.stop_ = False
        self.minutes_arry = []
        self.sorted_files_names = []
    def on_mousewheel(self,event):
        self.scrolling_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def close(self):
        self.main_root.destroy()
    def entry_onhover(self,e):
        if self.search_text.get() == "Example: 02-27-2024_18-11-34":
            self.search_text.set("")

    def start_checking(self,e):
        for label,button in zip(self.labels,self.buttons):
            label.destroy()
            button.destroy()
        self.labels.clear()
        self.buttons.clear()
        def return_str():
            if len(self.search_text.get()) != 0 and (self.search_text.get()[-1] == "_" or self.stop_):
                if '_' not in self.search_text.get():
                    self.stop_ = False
                    self.second_searh.clear()
                else:
                    self.second_searh= [x for x in self.search_text.get()[self.search_text.get().index("_")+1:].split('-') if x != '' and len(x) > 1 and x.isdigit() and len(x) <5 ]
                    self.stop_ = True
            else:
                if '_' not in self.search_text.get():
                    self.stop_ = False
                if self.stop_:
                    self.first_search=[x for x in self.search_text.get()[:self.search_text.get().index("_")].split('-') if x !='' and len(x)>1 and x.isdigit()  and len(x) < 5 ]
                else:
                    self.first_search=[x for x in self.search_text.get().split('-') if x !='' and len(x)>1 and x.isdigit()  and len(x) < 5 ]
                    for i,x in enumerate(self.first_search):
                        if i == 2:
                            if len(x) != 4:
                                self.first_search.remove(x)
            # if len(self.first_search) > 3:
        return_str()
        if self.option.get() == "Videos":
            def start_search(year):
                month_dirs = [os.path.join(year, x) for x in os.listdir(year)]
                stop_month = False
                for month_dir in month_dirs:
                    if len(self.first_search) >= 1 and self.first_search[0] == month_dir[-2:]:
                        self.current_month = month_dir
                        stop_month = True
                        break
                if stop_month:
                    day_dirs = [os.path.join(self.current_month, x) for x in os.listdir(self.current_month) if os.path.isdir(os.path.join(self.current_month,x))]
                    stop_day = False
                    for day_dir in day_dirs:
                        if len(self.first_search) >= 2 and day_dir[-2:] == self.first_search[1]:
                            self.current_day = day_dir
                            files = os.listdir(self.current_day)
                            files_by_creation_time = [(file, os.path.getctime(os.path.join(self.current_day,file))) for file in files]
                            sorted_files = sorted(files_by_creation_time, key=lambda x: x[1])
                            self.sorted_files_names =  [file[0] for file in sorted_files]
                            print(self.current_day)
                            stop_day = True
                            break
                    if len(self.first_search)>=2 and not stop_day:
                        return
                    if stop_day:
                        if len(self.second_searh) == 1:
                            self.minutes_arry.clear()
                            for index, f in enumerate(self.sorted_files_names, start=1):
                                if self.second_searh[0] == f.split('_')[1][:2]:
                                    label = Label(self.canvas_frame, text=f, font=("Times New Roman", 20))
                                    label.grid(row=index, column=0,pady=5,padx=40)
                                    button = Button(self.canvas_frame, text="open", font=("Times New Roman", 15),command=lambda vid=f:self.create_window(os.path.join(self.current_day,vid),vid))
                                    button.grid(row=index, column=1, pady=5)
                                    self.labels.append(label)
                                    self.buttons.append(button)
                                    self.minutes_arry.append(f)
                        elif len(self.second_searh) == 2:
                            for index, f in enumerate(self.minutes_arry, start=1):
                                if self.second_searh[0] == f.split('_')[1][:2] and self.second_searh[1] == f.split('_')[1][3:5]:
                                    label = Label(self.canvas_frame, text=f, font=("Times New Roman", 20))
                                    label.grid(row=index, column=0,pady=5,padx=40)
                                    button = Button(self.canvas_frame, text="open", font=("Times New Roman", 15), command=lambda vid=f:self.create_window(os.path.join(self.current_day,vid),vid))
                                    button.grid(row=index, column=1, pady=5)
                                    self.labels.append(label)
                                    self.buttons.append(button)
                        else:
                            for index, f in enumerate(self.sorted_files_names, start=1):
                                label = Label(self.canvas_frame, text=f, font=("Times New Roman", 20))
                                label.grid(row=index, column=0,pady=5,padx=40)
                                button = Button(self.canvas_frame, text="open", font=("Times New Roman", 15),command=lambda vid=f:self.create_window(os.path.join(self.current_day,vid),vid))
                                button.grid(row=index, column=1, pady=5)
                                self.labels.append(label)
                                self.buttons.append(button)
                    else:
                        s = 1
                        for day_dir in day_dirs:
                            files = os.listdir(day_dir)
                            files_by_creation_time = [(file, os.path.getctime(os.path.join(day_dir, file))) for file in files]
                            sorted_files = sorted(files_by_creation_time, key=lambda x: x[1])
                            sorted_files_names = [file[0] for file in sorted_files]
                            for index, f in enumerate(sorted_files_names, start=s):
                                label = Label(self.canvas_frame, text=f, font=("Times New Roman", 20))
                                label.grid(row=index, column=0,pady=5,padx=40)
                                button = Button(self.canvas_frame, text="open", font=("Times New Roman", 15),command=lambda vid=f:self.create_window(os.path.join(day_dir,vid),vid))
                                button.grid(row=index, column=1,pady=5)
                                self.buttons.append(button)
                                self.labels.append(label)
                                s += 1

            year_dirs = [os.path.join(self.parent_dir,x) for x in os.listdir(self.parent_dir)]
            if len(self.first_search):
                stop_year = False
                for year_dir in year_dirs:
                    if len(self.first_search) >=3 and year_dir[-4:] == self.first_search[2]:
                        self.current_year = year_dir
                        stop_year = True
                        break
                if stop_year:
                    start_search(self.current_year)
                else:
                    for year_dir in year_dirs:
                        start_search(year_dir)

    def create_window(self,video,vid):
        self.new_window = Toplevel(self.main_root)
        self.new_window.title(f"Video {vid}")
        self.new_window.resizable(False, False)
        self.new_window.geometry("700x600")

        show_video = show_video_tapes(self.new_window,video)
        review_thread = threading.Thread(target=show_video.on_button_click)
        review_thread.start()
        self.new_window.protocol("WM_DELETE_WINDOW", show_video.stop)
        show_video.update_gui()
        self.new_window.mainloop()



class show_video_tapes:
    def __init__(self,window,video):
        self.window = window
        self.path_to_vid = video
        self.cap = cv2.VideoCapture(self.path_to_vid)
        if not self.cap.isOpened():
            print("Nothing")
        self.stop_event = threading.Event()
        self.queue = Queue()
        self.fps = 20.0
        self.delay = int(10000/self.fps)
        self.frame_label = Label(self.window)
        self.paused = False
        self.display_paused = False

        self.pause_button = Button(self.window, text="Pause", command=self.pause_video, font=("Helvetica", 15),fg='red',bg='black')
        self.pause_button.grid(row=1,column=1)

        self.frames_array = []
        self.go_back = False
        self.reversed_button = Button(self.window, text="<<", font=("Helvetica",15), fg='red', bg='black',command=self.go_back)
        self.reversed_button.grid(row=1, column=0)

    def go_back(self):
        self.go_back = not self.go_back
    def go_back_functionality(self):
        pass
        

    def pause_video(self):
        self.paused = not self.paused
        self.display_paused = not self.display_paused
    def on_button_click(self):
        while not self.stop_event.is_set():
            if not self.paused:
                # if self.go_back:

                ret,frame = self.cap.read()
                if not ret:
                    break
                self.frames_array.append(frame)
                self.queue.enqueue(frame)
                time.sleep(0.030)

    def stop(self):
        self.cap.release()
        self.stop_event.set()
        self.window.destroy()


    def update_gui(self,):
        if not self.queue.is_empty() and not self.display_paused and not self.stop_event.is_set():
            frame = self.queue.dequeue()# Get the latest frame
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)
            image = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=image)
            self.frame_label.configure(image=imgtk)
            self.frame_label.grid(row=0,column=0)
            self.frame_label.image = imgtk  # Keep a reference!
        self.window.after(20,self.update_gui)


class Queue:
    def __init__(self,buffer=None):
        self.buffer = deque()
        self.max_size = 2
    def enqueue(self, val):
        if len(self.buffer) >= self.max_size:
            self.buffer.popleft()
        self.buffer.appendleft(val)
    def dequeue(self):
        if not self.is_empty():
            return self.buffer.pop()
    def is_empty(self):
        return len(self.buffer) == 0
    def size(self):
        return len(self.buffer)

class Detect_Queue(Queue):
    pass
class Record_Queue(Queue):
    pass

# date: 11-02-2024
# time: 18-47-59
def make_dirs(latest_year,latest_day,latest_date,next):
    if int(latest_year) < int(next[2]):
        os.makedirs(f"C:\\Users\\haram\\PycharmProjects\\motionDetection\\videos\\{next[2]}\\{next[1]}{next[0]}", exist_ok=True)
        return f'C:\\Users\\saler\\Desktop\\Programing\\motionDetection\\videos\\{next[2]}\\{next[1]}{next[0]}'
    if int(latest_date) < int(next[1]):
            os.makedirs(f"C:\\Users\\haram\\PycharmProjects\\motionDetection\\videos\\{latest_year}\\{next[1]}\\{next[0]}",exist_ok=True)
            return f'C:\\Users\\saler\\Desktop\\Programing\\motionDetection\\videos\\{latest_year}\\{next[1]}\\{next[0]}'
    elif int(latest_day) < int(next[0]):
            os.makedirs(f"C:\\Users\\haram\\PycharmProjects\\motionDetection\\videos\\{latest_year}\\{latest_date}\\{next[0]}",exist_ok=True)
            return f'C:\\Users\\haram\\PycharmProjects\\motionDetection\\videos\\{latest_year}\\{latest_date}\\{next[0]}'
    elif int(latest_day) == int(next[0]) and int(latest_date) == int(next[1]) and int(latest_year) ==int(next[2]):
        return f"C:\\Users\\haram\\PycharmProjects\\motionDetection\\videos\\{latest_year}\\{latest_date}\\{latest_day}"

def make_empty_dirs():
    year_path = "C:\\Users\\haram\\PycharmProjects\\motionDetection\\videos"
    all_entries = os.listdir(year_path)
    year_dirs = [entry for entry in all_entries if os.path.isdir(os.path.join(year_path, entry))]
    next = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    date,_ = next.split("_")
    date= date.split('-')
    if year_dirs:
        latest_year_dir = year_dirs[-1]
        month_path = f"C:\\Users\\haram\\PycharmProjects\\motionDetection\\videos\\{latest_year_dir}"
        all_month_entries = os.listdir(month_path)
        month_dirs = [entry for entry in all_month_entries if os.path.isdir(os.path.join(month_path, entry))]
        if month_dirs:
            latest_month_dir = month_dirs[-1]
            day_path = f"C:\\Users\\haram\\PycharmProjects\\motionDetection\\videos\\{latest_year_dir}\\{latest_month_dir}"
            all_days_entries = os.listdir(day_path)
            day_dirs = [entry for entry in all_days_entries if os.path.isdir(os.path.join(day_path,entry))]
            if day_dirs:
                latest_day_dir = day_dirs[-1]
                return make_dirs(latest_year_dir,latest_day_dir,latest_month_dir,date)
            else:
                os.makedirs(
                    f"C:\\Users\\haram\\PycharmProjects\\motionDetection\\videos\\{latest_year_dir}\\{latest_month_dir}\\{date[0]}",
                    exist_ok=True)
                return f"C:\\Users\\haram\\PycharmProjects\\motionDetection\\ideos\\{latest_year_dir}\\{latest_month_dir}\\{date[0]}"
        else:
            os.makedirs(f"C:\\Users\\haram\\PycharmProjects\\motionDetection\\videos\\{latest_year_dir}\\{date[1]}\\{date[0]}",exist_ok=True)
            return f"C:\\Users\\haram\\PycharmProjects\\motionDetection\\ideos\\{latest_year_dir}\\{date[1]}\\{date[0]}"
    else:
        os.makedirs(f"C:\\Users\\haram\\PycharmProjects\\motionDetection\\videos\\{date[2]}\\{date[1]}\\{date[0]}", exist_ok=True)
        return f"C:\\Users\\haram\\PycharmProjects\\motionDetection\\videos\\{date[2]}\\{date[1]}\\{date[0]}"

def file_handler():
    directory = make_empty_dirs()

    files = [os.path.join(directory, f) for f in os.listdir(directory) if
             os.path.isfile(os.path.join(directory, f))]
    now = datetime.now()
    now = now.strftime("%m-%d-%Y_%H-%M-%S")
    files.sort(key=os.path.getctime, reverse=True)
    if files:
        latest_file = files[0]
        latest = latest_file.split("\\")[-1]
        latest_int = int(latest[latest.index("o") + 1:latest.find("(")]) + 1
        return f"{directory}\\video{latest_int}({now}).avi"
    else:
        return f"{directory}\\video0({now}).avi"
def delete_dir(path):
    shutil.rmtree(path)




def options_video(cap, flag=False):
    filename = file_handler()
    frames_per_second = 20.0
    res = '480p'
    def change_res(cap, width, height):
        cap.set(3,width)
        cap.set(4,height)

    STD_DIMENSIONS = {
        "480p": (640, 480),
        "720p": (1280, 720),
        "1080p": (1920, 1010),
        "4k": (3840, 2160),
    }
    def get_dims(cap, res="720p"):
        width, height = STD_DIMENSIONS['480p']
        if res in STD_DIMENSIONS:
            width, height = STD_DIMENSIONS[res]
        if not flag:
            change_res(cap,width,height)
        return width, height
    dims = get_dims(cap, res=res)

    VIDEO_TYPE = {
        'avi': cv.VideoWriter_fourcc(*'XVID'),
        # 'mp4': cv2.VideoWriter_fourcc(*'H264'),
        'mp4': cv.VideoWriter_fourcc(*'XVID'),
        "mjpg":cv.VideoWriter_fourcc(*"MJPG"),
    }

    def get_video_type(filename):
        filename, ext = os.path.splitext(filename)
        if ext in VIDEO_TYPE:
            return VIDEO_TYPE[ext]
        return VIDEO_TYPE['avi']
    video_type_cv2 = get_video_type(filename)
    out = cv.VideoWriter(filename, video_type_cv2, frames_per_second, dims)
    return out
class detect_and_Record:
    def __init__(self,main_window,camera_index):
        self.main_window = main_window
        self.is_recording = False
        self.not_recording = True
        self.current_dir = None
        self.camera = None
        self.camera_index = camera_index
        self.haar_cascade = cv.CascadeClassifier('cascades/haar_face.xml')
        self.display_queue = Queue()
        self.stop_event = threading.Event()
        self.capture = cv.VideoCapture(camera_index)
        self.detection_back = cv.createBackgroundSubtractorMOG2(history=100, varThreshold=40)
        if not self.capture.isOpened():
            print("Something went wrong")
        self.record = options_video(self.capture)
        # ------------------------------------------------------
        # self.record_thread = threading.Thread(target=self.record_video)
        # self.detect_thread = threading.Thread(target=self.detect)
        # self.file_dir_handle = threading.Thread(target=options_video)
        # --------------------------------------------------------------
        self.pre_timeframe = 0
        self.take_photo = False
        self.frame_label = Label(self.main_window)
        # Window widgets
        self.photo_button = Button(main_window, text="Make Photo", fg="red", background='black', font=("Times New Roman", 15),
                              command=self.make_photo)
        self.photo_button.grid(row=1, column=0,pady=10, ipadx=20,ipady=20,sticky='sw')
        self.photo_button.bind("<Enter>", lambda e:self.photo_button_on(e))
        self.photo_button.bind("<Leave>", lambda e: self.photo_button_off(e))

    def photo_button_on(self,e):
        self.photo_button.config(fg='black',background="red")
    def photo_button_off(self,e):
        self.photo_button.config(fg='red',background='black')
    def capture_frames(self):
        self.update_gui()
        duration = 10
        current_time = None
        start_time = True
        while not self.stop_event.is_set():
            ret, frame = self.capture.read()
            if not ret:
                print("Error: Can't receive frame. Exiting...")
                break
            if self.take_photo:
                self.photo_handler(frame)
                self.take_photo = False

            if self.is_recording:
                self.record.write(frame)
                # This if statement is when the current time is set
                if start_time:
                    current_time = time.time()
                    start_time = False
                # This if is when 10 seconds passes
                if int(time.time()) - int(current_time) >= duration:
                    self.is_recording = False
                    self.not_recording = True
                    start_time = True
                    self.record.release()
                    self.record = options_video(self.capture, flag=True)
            find_countorurs = False
            # Image filtering
            gray_frame = cv.cvtColor(frame, cv.COLOR_BGRA2GRAY)
            mask = self.detection_back.apply(frame)
            # ret,threshold = cv.threshold(gray_frame,125,255,cv.THRESH_BINARY)
            # hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            # rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            c, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            for cnt in c:
                area = cv.contourArea(cnt)
                if area > 500:
                    x, y, w, h = cv.boundingRect(cnt)
                    cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

                    find_countorurs = True
            if self.not_recording and find_countorurs:
                self.is_recording = True
                self.not_recording = False
            if self.is_recording:
                cv.circle(frame, (40, 60), 20, (0, 0, 255), -1)
            self.pre_timeframe = self.print_Frames(frame, self.pre_timeframe)
            self.display_queue.enqueue(frame)
            # ------------------------------------------------------
        self.capture.release()
        self.record.release()
        cv.destroyAllWindows()

    def update_gui(self):
        if not self.display_queue.is_empty():
            frame = self.display_queue.dequeue()# Get the latest frame
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)
            image = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=image)
            self.frame_label.configure(image=imgtk)
            self.frame_label.grid(row=0,column=0)
            self.frame_label.image = imgtk  # Keep a reference!
        self.main_window.after(20, self.update_gui)

    def photo_handler(self,frame):
        now = datetime.now()
        now = now.strftime("%d-%m-%Y_%H-%M-%S")
        cv.imwrite(f"photos\photo({now}).jpg",frame)
    def make_photo(self):
        self.take_photo = True


    def stop_cameras(self):
        self.stop_event.set()
        self.main_window.destroy()
        secondary.camera_button.configure(state=NORMAL, fg='red', background='black')
        secondary.camera_entry_button.configure(state=NORMAL, fg='red', background='black')
        secondary.connect_button.grid_forget()
        secondary.connect_button.configure(state=NORMAL, fg='red', background='black')
        secondary.camera_list.clear()
        for label in secondary.removable_labels:
            label.grid_forget()

    def print_Frames(self, frame, pre_timeframe):
        new_timeframe = time.time()
        fps = int(1 / (new_timeframe - pre_timeframe))
        pre_timeframe = new_timeframe
        cv.putText(frame, f"FPS: {fps}", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
        return pre_timeframe

def start_cameras(main_window):
    for i in secondary.camera_list:
        setup(main_window,i)



def setup(main_window, i):
    window = Toplevel(main_window)
    window.title(f"Camera {i}")
    window.geometry("700x600")
    window.resizable(False, False)

    camera = detect_and_Record(window, i)
    capture_thread = threading.Thread(target=camera.capture_frames)
    capture_thread.start()

    window.protocol("WM_DELETE_WINDOW", camera.stop_cameras)
    window.mainloop()

root.mainloop()