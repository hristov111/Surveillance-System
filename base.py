from tkinter import *
from tkinter import messagebox

root = Tk()
root.title("Kali 1.0")
root.geometry("600x600")
root.config(background='black')

default_pass = "pass"
default_user = "user"
# Main label
main_label = Label(root, text="Welcome to Kali motion by Kalata", border=2, font=("Time New Roman", 20))
main_label.pack()
# Frame
frame = LabelFrame(root, padx=50, pady=30, border=5)
frame.pack(padx=10, pady=150)
# user_label
username_label = Label(frame, text="Username:",border=2,font=("Times New Roman", 15))
username_label.pack()
# user-typing
user = StringVar()
# user entry
username_entry = Entry(frame,width=20, textvariable=user,border=5,font=('Helvetica', 15))
username_entry.pack()
# pass label
password_label = Label(frame, text="Password:",border=2,font=("Times New Roman", 15))
password_label.pack()
# pass-typing
password = StringVar()
# pass entry
password_entry = Entry(frame,width=20, textvariable=password,border=5,font=('Helvetica', 15))
password_entry.pack()
def check_credentials():
    if password.get() == default_pass and user.get() == default_user:
        print("ok")
    else:
        popUp()
        password.set("")
        user.set("")
def popUp():
    messagebox.showerror("Error", "username or password incorrect.Please try again")

continue_butt = Button(frame, text="Continue", font=("Arial", 15), width=15,command=check_credentials)
continue_butt.pack()
def on_enter(e):
    exit_button.config(background='black', fg="red")


def on_leave(e):
    exit_button.config(background="red", fg='black')

exit_button = Button(root, text="EXIT", command=root.destroy,width=10, background='black',fg='red',font=("Times New Roman",10))
exit_button.pack(side=BOTTOM, anchor='w')
exit_button.bind("<Enter>", on_enter)
exit_button.bind("<Leave>", on_leave)


root.mainloop()