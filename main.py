from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for letter in range(randint(8, 10))]
    password_list += [choice(symbols) for symbol in range(randint(2, 4))]
    password_list += [choice(numbers) for number in range(randint(2, 4))]

    shuffle(password_list)

    password = "".join(char for char in password_list)

    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ------------------------------ SAVE PASSWORD -------------------------------- #
def field_empty():
    return messagebox.showwarning(title="Oops!", message="Please do not leave any fields empty")

def add_clicked():
    website = website_entry.get().title()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {website: {
        "email": email,
        "password": password
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0: 
        field_empty()
    else:
        asking_to_save = messagebox.askokcancel(title="Saving Entry Data", message=f"These are the details entered:\n"
                                                f"Website: {website.title()}\nEmail: {email}\nPassword: {password}\n Is it OK to save?")
        if asking_to_save:
            try: 
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)
                    data.update(new_data)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                with open("data.json", "w") as _data:
                    json.dump(data, _data, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)

# ------------------------------ FIND PASSWORD -------------------------------- #
def search_clicked():
    website = website_entry.get().title()
    email = email_entry.get()

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="File not Found", message="Data file not found\n"
                                  "Input entries then click Add and Save first!")
    else:
        if website in data:
            temp = data[website]
            messagebox.showinfo(title=f"Detail info for {website}\n", 
                                message=f"Email: {temp['email']}\n"
                                f"Password: {temp['password']}")
        else: 
            messagebox.showinfo(title="Data not Found", message=f"No details for {website} exists!")
        
# ------------------------------- UI SETUP ----------------------------------- #

# Screen and Canvas Setting
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=30, bg="white")

canvas = Canvas(height=200, width=200, bg="white")
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Website 
website_label = Label(text="Website:", bg="white")
website_label.grid(row=1, column=0, pady=5)
email_label = Label(text="Email/Username:", bg="white")
email_label.grid(row=2, column=0, pady=5)
password_label = Label(text="Password:", bg="white")
password_label.grid(row=3, column=0, pady=5)

# Widget Entry
website_entry = Entry(width=34)
website_entry.grid(row=1, column=1, pady=5)
website_entry.focus()
email_entry = Entry(width=54)
email_entry.grid(row=2, column=1, columnspan=2, pady=5)
email_entry.insert(0, "youremail@domain.com") # Set pre-value to your own email
password_entry = Entry(width=34)
password_entry.grid(row=3, column=1, pady=5)

# Widget Button
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2, pady=5)
add_button = Button(text="Add and Save", width=46, command=add_clicked)
add_button.grid(row=4, column=1, columnspan=2, pady=5)
search_button = Button(text="Search", width=15, command=search_clicked)
search_button.grid(row=1, column=2, pady=5)

window.mainloop()
