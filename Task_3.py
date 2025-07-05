import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

CONTACTS_FILE = "contacts.json"

# Load contacts from file
def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "r") as file:
            return json.load(file)
    return []

# Save contacts to file
def save_contacts(contacts):
    with open(CONTACTS_FILE, "w") as file:
        json.dump(contacts, file, indent=4)

# Main GUI App
class ContactManager:
    def __init__(self, root):
        self.root = root
        self.root.title("📇 Contact Manager")
        self.contacts = load_contacts()

        self.frame = tk.Frame(root, padx=10, pady=10)
        self.frame.pack()

        self.listbox = tk.Listbox(self.frame, width=50)
        self.listbox.pack(pady=10)
        self.load_listbox()

        tk.Button(self.frame, text="Add Contact", width=15, command=self.add_contact).pack(pady=2)
        tk.Button(self.frame, text="Edit Contact", width=15, command=self.edit_contact).pack(pady=2)
        tk.Button(self.frame, text="Delete Contact", width=15, command=self.delete_contact).pack(pady=2)
        tk.Button(self.frame, text="Refresh List", width=15, command=self.load_listbox).pack(pady=2)

    def load_listbox(self):
        self.listbox.delete(0, tk.END)
        for idx, contact in enumerate(self.contacts):
            self.listbox.insert(tk.END, f"{idx+1}. {contact['name']} | {contact['phone']} | {contact['email']}")

    def add_contact(self):
        name = simpledialog.askstring("Name", "Enter contact name:")
        phone = simpledialog.askstring("Phone", "Enter phone number:")
        email = simpledialog.askstring("Email", "Enter email address:")

        if name and phone and email:
            self.contacts.append({"name": name, "phone": phone, "email": email})
            save_contacts(self.contacts)
            self.load_listbox()
            messagebox.showinfo("Success", "Contact added successfully.")
        else:
            messagebox.showwarning("Input Error", "All fields are required.")

    def edit_contact(self):
        index = self.listbox.curselection()
        if not index:
            messagebox.showwarning("Selection Error", "Please select a contact to edit.")
            return
        i = index[0]
        contact = self.contacts[i]

        name = simpledialog.askstring("Name", "Edit name:", initialvalue=contact['name'])
        phone = simpledialog.askstring("Phone", "Edit phone:", initialvalue=contact['phone'])
        email = simpledialog.askstring("Email", "Edit email:", initialvalue=contact['email'])

        if name and phone and email:
            self.contacts[i] = {"name": name, "phone": phone, "email": email}
            save_contacts(self.contacts)
            self.load_listbox()
            messagebox.showinfo("Updated", "Contact updated successfully.")
        else:
            messagebox.showwarning("Input Error", "All fields are required.")

    def delete_contact(self):
        index = self.listbox.curselection()
        if not index:
            messagebox.showwarning("Selection Error", "Please select a contact to delete.")
            return
        i = index[0]
        contact = self.contacts[i]
        confirm = messagebox.askyesno("Confirm Delete", f"Delete contact: {contact['name']}?")
        if confirm:
            self.contacts.pop(i)
            save_contacts(self.contacts)
            self.load_listbox()
            messagebox.showinfo("Deleted", "Contact deleted successfully.")

# Run the App
if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManager(root)
    root.mainloop()
