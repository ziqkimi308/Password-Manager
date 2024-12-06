"""
********************************************************************************
* Project Name:  Password Manager
* Description:   The Password Manager is a secure and efficient Python application built with Tkinter
* Author:        ziqkimi308
* Created:       2024-12-05
* Updated:       2024-12-05
* Version:       1.0
********************************************************************************
"""

from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# CONST
JSON_PATH = r"./data.json"
LOGO_PATH = r"./logo.png"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
	letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
	numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
	symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

	# Choose random length for letters, symbols, and numbers
	nr_letters = random.randint(8, 10)
	nr_symbols = random.randint(2, 4)
	nr_numbers = random.randint(2, 4)

	# Append letters, symbols, and numbers into password list and shuffle the list
	# password_list = []
	# for char in range(nr_letters):
	#   password_list.append(random.choice(letters))

	# for char in range(nr_symbols):
	#   password_list += random.choice(symbols)

	# for char in range(nr_numbers):
	#   password_list += random.choice(numbers)

	# Replace older long codes using this shorter line comprehensions
	password_list = (
		[random.choice(letters) for char in range(nr_letters)] +
		[random.choice(symbols) for char in range(nr_symbols)] +
		[random.choice(numbers) for char in range(nr_numbers)]
	)

	random.shuffle(password_list)

	# Convert list to string
	password = "".join(password_list)
	entry_password.delete(0, END)
	entry_password.insert(0, password)
	pyperclip.copy(password)

	print(f"Your password is: {password}")

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
	# Collect data from each entries
	website = entry_website.get().lower()
	email = entry_email_username.get().lower()
	password = entry_password.get()
	new_data = {
		website: {
			"email": email,
			"password": password
		}
	}

	if len(website) == 0 or len(password) == 0:
		messagebox.showinfo(title="Oops", message="Please makes sure you to fill every field.")
	else:
		try:
			with open(JSON_PATH, "r") as data_file:
				# Read old data
				data = json.load(data_file)

		except FileNotFoundError:
			with open(JSON_PATH, "w") as data_file:
				json.dump(new_data, data_file, indent=4)
		
		else:
			# Update old data with new data
			data.update(new_data)

			# Save updated data
			with open(JSON_PATH, "w") as data_file:
				json.dump(data, data_file, indent=4)
	
		finally:
			# Clear each entries
			entry_website.delete(0, END)
			entry_password.delete(0, END)

# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
	website_get = entry_website.get().lower()
	try:
		with open(JSON_PATH, "r") as data_file:
			data = json.load(data_file)

	except FileNotFoundError:
		messagebox.showinfo(message="No Data File Found")

	else:
		if website_get in data:
			email = data[website_get]["email"]
			password = data[website_get]["password"]
			messagebox.showinfo(title=website_get, message=f"Email: {email}\nPassword: {password}")
		else:
			messagebox.showinfo(title="Oops", message="No details for the website exists")

# ---------------------------- UI SETUP ------------------------------- #
# Tk
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Canvas
canvas = Canvas(width=200, height=200)
logo_image = PhotoImage(file=LOGO_PATH)
canvas.create_image(100, 100, image=logo_image)
canvas.grid(row=0, column=1)

# Label
label_website = Label(text="Website:")
label_website.grid(row=1, column=0)

label_email_username = Label(text="Email/Username:")
label_email_username.grid(row=2, column=0)

label_password = Label(text="Password:")
label_password.grid(row=3, column=0)

# Entry
entry_website = Entry(width=33)
entry_website.grid(row=1, column=1, columnspan=2, sticky="w")
entry_website.focus()

entry_email_username = Entry(width=51)
entry_email_username.grid(row=2, column=1, columnspan=2, sticky="w")
# To auto insert default email at start
entry_email_username.insert(0, "haziqhakimiyes@gmail.com")

entry_password = Entry(width=33)
entry_password.grid(row=3, column=1, sticky="w")

# Button
button_search = Button(text="Search", command=find_password)
button_search.grid(row=1, column=2, sticky="we")

button_generate_pass = Button(text="Generate Password", command=generate_password)
button_generate_pass.grid(row=3, column=2, sticky="we")

button_add = Button(text="Add", width=43, command=save)
button_add.grid(row=4, column=1, columnspan=2, sticky="w")

# Last
window.mainloop()