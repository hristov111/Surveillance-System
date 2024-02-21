
from tkinter import *
from tkinter import messagebox
import cv2 as cv
import time
import threading
import sqlite3
import bcrypt
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
    def update_user(self,username, password):
       pass
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


class Main_Screen:
    def __init__(self,root):
        self.root = root
        self.root.config(background="black")
        self.default_pass = "pass"
        self.default_user = "user"
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
        self.is_lower = False
        self.is_upper = False
        self.is_number = False
        self.is_eight = False
        self.confirmed_password = False
        self.confirmed_username = False
        self.database = connect_database()
    def create_account(self):
        account_window = Toplevel(self.root)
        account_window.title("Create account")
        account_window.geometry("500x500")
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
            self.is_lower = False
            self.is_upper = False
            self.is_number = False
            self.is_eight = False
            if len(current) == 8:
                eight_characters_label.config(text="✅ password must contain 8 characters")
                self.is_eight = True
            else:
                eight_characters_label.config(text="❌ password must contain 8 characters")
            for word in current:
                if word.islower():
                    self.is_lower = True
                elif word.isupper():
                    self.is_upper = True
                elif word.isdigit():
                    self.is_number = True
            if self.is_lower:
                one_lowercase_letter.config(text="✅ password must contain at least one lowercase letter")
            else:
                one_lowercase_letter.config(text="❌ password must contain at least one lowercase letter")
            if self.is_upper:
                one_uppercase_letter.config(text="✅ password must contain at least one uppercase letter")
            else:
                one_uppercase_letter.config(text="❌  password must contain at least one uppercase letter")
            if self.is_number:
                one_digit.config(text="✅ password must contain one digit")
            else:
                one_digit.config(text="❌ password must contain one digit")

        def check_confirmed_pass(e):
            self.confirmed_password = False
            if password.get() != confirm_password.get():
                confirmation_password_label.grid(row=4, column=1, sticky="W", pady=15)
                self.confirmed_password = True
            else:
                confirmation_password_label.grid_forget()

        def check_user_exists(e,entry):
            self.confirmed_username = False
            username = entry.get()
            is_checked = self.database.check_user(username)
            if is_checked:
                self.confirmed_username = True
                user_name_wrong.grid(row=2,column=1,columnspan=2,pady=10)
            else:
                user_name_wrong.grid(row=2, column=1)
        def check_username(e,entry):
            username = entry.get()
            first_check = False
            second_check = False
            third_check = False
            if "$" in username or "@" in username or  "_" in username:
                first_check = True



        user_name_label = Label(account_window, text="username: ", font=("Times New Roman", 15))
        user_name_label.grid(row=1, column=0, pady=15, sticky="W")
        username_entry = Entry(account_window, textvariable=username, font=("Times New Roman", 15), border=5,width=30)
        username_entry.bind("<Button-1>", lambda e, entry=username_entry:entry_onhover(e,entry))
        username_entry.bind("<KeyRelease>", lambda e, entry=username_entry:check_user_exists(e,username_entry))

        username_check_characters = Label(account_window, text="❌ Max. 10 characters allowed:\n$ @ _ a-z 1-9 ", font=("Times New Roman"))
        username_entry.bind("KeyRelease", lambda e, entry=username_entry: check_username)
        username_entry.insert(0, "HeHeHohoHiHi")
        username_entry.grid(row=1, column=1)

        password_label = Label(account_window, text="password: ", font=("Times New Roman", 15))
        password_label.grid(row=3, column=0, sticky="W")
        password_entry = Entry(account_window, textvariable=password, font=("Times New Roman", 15), border=5,width=30)
        password_entry.bind("<Button-1>",  lambda e,entry=password_entry:password_onhover(e,entry))
        password_entry.bind("<KeyRelease>", check_password)
        password_entry.grid(row=3, column=1,pady=10)

        confirm_password_label = Label(account_window, text="confirm password: ", font=("Times New Roman", 15))
        confirm_password_label.grid(row=4, column=0, sticky="W")
        confirm_password_entry = Entry(account_window, textvariable=confirm_password, font=("Times New Roman", 15), border=5,width=30)
        confirm_password_entry.bind("<Button-1>", lambda e,entry=confirm_password_entry:password_onhover(e,entry))
        confirm_password_entry.grid(row=4, column=1, pady=5)
        confirm_password_entry.bind("<KeyRelease>" ,check_confirmed_pass)

        eight_characters_label = Label(account_window, text="❌ password must contain 8 characters")
        eight_characters_label.grid(row=5,column=1, sticky="W")
        one_uppercase_letter = Label(account_window, text="❌ password must contain at least one uppercase letter")
        one_uppercase_letter.grid(row=6,column=1,sticky="W")
        one_lowercase_letter = Label(account_window, text="❌ password must contain at least one lowercase letter")
        one_lowercase_letter.grid(row=7,column=1,sticky="W")
        one_digit = Label(account_window, text="❌ password must contain one digit")
        one_digit.grid(row=8, column=1, sticky="W")

        confirmation_password_label = Label(account_window, text="Password doesn't match", font=("Times New Roman", 15), background='red')
        # confirmation_password_label.grid(row=4, column=1, sticky="W", pady=15)
        confirmation_password_label.bind("<KeyRelease>", check_confirmed_pass)
        user_name_wrong = Label(account_window, text="Username is taken!",font=("Times New Roman", 15), background='red')

        submit_butt = Button(account_window, text="Save changes", font=("Times New Roman", 15), fg='green')
        submit_butt.bind("<Enter>", onhover)
        submit_butt.bind("<Leave>", outhover)
        submit_butt.grid(row=9, column=0, columnspan=2, pady=15, padx=15, ipadx=20, ipady=10)




        account_window.mainloop()

    def check_credentials(self):
        if self.password.get() == self.default_pass and self.user.get() == self.default_user:
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
    root2.title("Camera Detection Page")
    root2.geometry("640x480")
    secondary = Secondary_Page(root2)
    root2.protocol("WM_DELETE_WINDOW", secondary.close_window)
    root2.mainloop()

class Secondary_Page:
    def __init__(self,root2):
        self.root2 = root2
        self.camera_entry_label = Label(root2, text="Enter the number of cameras", font=("Times New Roman", 15))
        self.camera_entry_label.pack()
        self.cameras_entry_var = IntVar()
        self.camera_button = None
        self.clicked = 0
        self.label_array,self.camera_entries,self.entry_array,self.entry_vars = [],[],[],[]
        self.cameras_entry = Entry(root2, textvariable=self.cameras_entry_var, width=20, font=("Helvetica", 15))
        self.cameras_entry.pack()
        self.camera_entry_button = Button(root2, text="Submit", width=10, font=("Times New Roman", 15),
                                     command=self.create_indices)
        self.camera_entry_button.pack()
        self.camera_button = Button(root2)
        self.change_user_pass_butt = Button(root2, text="Change username \nand password", command=self.change_password_username, font=("Times New Roman",13))
        self.change_user_pass_butt.pack(side=BOTTOM, anchor='e',padx=10,pady=10)

    def change_password_username(self):
        change = Toplevel(self.root2)
        change.title("Change Password and Username")
        change.geometry("500x200")
        new_password = StringVar()

        # Create function for button hovering
        def onhover(e):
            submit_butt.config(fg='red')


        #     Create function for entry hovering
        def password_onhover(e):
            new_password_entry.delete(0, END)

        password_label = Label(change, text="new password: ", font=("Times New Roman", 15))
        password_label.grid(row=2, column=0, padx=50)
        new_password_entry = Entry(change, textvariable=new_password, font=("Times New Roman", 15),border=2)
        new_password_entry.bind("<Button-1>", password_onhover)
        new_password_entry.insert(0, "12345hello")
        new_password_entry.grid(row=2, column=1)

        confirm_password_label = Label(change, text="confirm new password: ", font=("Times New Roman", 15))
        confirm_password_label.grid(row=3, column=0, padx=20)
        confirm_new_password_entry = Entry(change, textvariable=new_password, font=("Times New Roman", 15), border=2)
        confirm_new_password_entry.bind("<Button-1>", password_onhover)
        confirm_new_password_entry.insert(0, "12345hello")
        confirm_new_password_entry.grid(row=3, column=1,pady=14)

        submit_butt = Button(change, text="Save changes", font=("Times New Roman" ,15),fg='green')
        submit_butt.bind("<Enter>",onhover)
        submit_butt.grid(row=4, column=0, columnspan=2, pady=15,padx=15, ipadx=20, ipady=10)




    def create_indices(self):
        if self.cameras_entry_var.get() >5:
            messagebox.showerror("Error", "The maximum number of cameras is 5")
            self.cameras_entry_var.set(0)
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
        for i in range(self.cameras_entry_var.get()):
            label = Label(self.root2, text="Index: ", font=("Times New Roman", 15))
            label.pack()
            index = IntVar()
            entry = Entry(self.root2, textvariable=index, font=("Times New Roman", 15))
            entry.pack()
            self.entry_vars.append(index)
            self.label_array.append(label)
            self.entry_array.append(entry)
        if self.cameras_entry_var.get() == 0:
            messagebox.showerror("Error", "Please select the number of cameras")
        if self.camera_button is not None:
            self.camera_button.destroy()
        if self.cameras_entry_var.get() != 0:

            self.camera_button = Button(self.root2, text="Submit",
                               font=("Times New Roman", 15), command=lambda : self.check_for_indices(self.entry_vars))
            self.camera_button.pack()

    def check_for_indices(self,list):
        camera_list = []
        # camera_entry_button.config(state=DISABLED)
        compared_list = set([i.get() for i in list])
        if len(compared_list) != len(list):
            messagebox.showerror("Error", "Please select two individual cameras")
            for var in self.entry_vars:
                var.set('')
            return
        for i in list:
            cap = cv.VideoCapture(i.get())
            index = i.get()
            if not cap.isOpened():
                messagebox.showerror("Error", f"Camera with index {index} does not exist.Please change indices")
                cap.release()
            else:
                checking1 = Label(self.root2, text="Checking please wait...", font=("Times New Roman", 15))
                checking1.pack()
                camera_list.append(index)
                self.root2.after(5000, lambda l=index: self.update_label_success(checking1, l))
        self.camera_button['state'] = DISABLED
        self.camera_entry_button['state'] = DISABLED
        self.start_cameras(camera_list)
    def update_label_success(self,label, index):
        label.config(text=f"Camera with index {index} is accessible! Success!")


    def close_window(self):
        self.root2.destroy()
        main.continue_butt.config(state=ACTIVE)
        main.password_entry.config(state=NORMAL)
        main.username_entry.config(state=NORMAL)
    def start_cameras(self,camera_list):
        pass

    def stop_cameras(self):
        pass







root.mainloop()