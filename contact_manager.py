import sqlite3
import tkinter as tk
from tkinter import messagebox


def create_table():
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS contacts
                 (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, email TEXT)''')
    conn.commit()
    conn.close()


create_table()


class ContactManager:
    def __init__(self, root):
        self.root = root
        self.root.title('Contact Manager')
        self.root.geometry('400x400')
        self.create_widgets()

    def create_widgets(self):
        # Create labels
        name_label = tk.Label(self.root, text="Name:")
        phone_label = tk.Label(self.root, text="Phone:")
        email_label = tk.Label(self.root, text="Email:")

        # Create entry fields
        self.name_entry = tk.Entry(self.root)
        self.phone_entry = tk.Entry(self.root)
        self.email_entry = tk.Entry(self.root)

        # Create add button
        add_button = tk.Button(self.root, text="Add Contact", command=self.add_contact)

        # delete button
        delete_button = tk.Button(self.root, text="Delete Contact", command=self.delete_contact)
        delete_button.grid(row=5, columnspan=2, padx=5, pady=5)

        # Create delete all button
        delete_all_button = tk.Button(self.root, text="Delete All Contacts", command=self.delete_all_contacts)
        delete_all_button.grid(row=6, columnspan=2, padx=5, pady=5)

        # Grid layout
        name_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        phone_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.phone_entry.grid(row=1, column=1, padx=5, pady=5)

        email_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.email_entry.grid(row=2, column=1, padx=5, pady=5)

        add_button.grid(row=3, columnspan=2, padx=5, pady=5)
        # Create listbox
        self.contact_listbox = tk.Listbox(self.root, width=40, height=10)
        self.contact_listbox.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Create scrollbar
        scrollbar = tk.Scrollbar(self.root)
        scrollbar.grid(row=4, column=2, sticky='ns')

        # Attach scrollbar to listbox
        self.contact_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.contact_listbox.yview)

        # Load contacts
        self.load_contacts()

    def add_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()

        if not name:
            messagebox.showerror("Error", "Name field is required.")
            return

        conn = sqlite3.connect('contacts.db')
        c = conn.cursor()
        c.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
        conn.commit()
        conn.close()

        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.load_contacts()
        messagebox.showinfo("Success", "Contact added successfully.")

    def load_contacts(self):
        conn = sqlite3.connect('contacts.db')
        c = conn.cursor()
        c.execute("SELECT * FROM contacts")
        contacts = c.fetchall()
        conn.close()

        self.contact_listbox.delete(0, tk.END)

        for contact in contacts:
            self.contact_listbox.insert(tk.END, f"{contact[1]} - {contact[2]} - {contact[3]}")

    def delete_contact(self):
        selected_contact = self.contact_listbox.curselection()

        if not selected_contact:
            messagebox.showerror("Error", "No contact selected.")
            return

        contact_data = self.contact_listbox.get(selected_contact[0]).split(' - ')
        name, phone, email = contact_data

        confirmation = messagebox.askyesno("Confirm", f"Are you sure you want to delete '{name}'?")

        if confirmation:
            conn = sqlite3.connect('contacts.db')
            c = conn.cursor()
            c.execute("DELETE FROM contacts WHERE name = ? AND phone = ? AND email = ?", (name, phone, email))
            conn.commit()
            conn.close()

            self.load_contacts()
            messagebox.showinfo("Success", "Contact deleted successfully.")

    def delete_all_contacts(self):
        confirmation = messagebox.askyesno("Confirm", "Are you sure you want to delete all contacts?")

        if confirmation:
            conn = sqlite3.connect('contacts.db')
            c = conn.cursor()
            c.execute("DELETE FROM contacts")
            conn.commit()
            conn.close()

            self.load_contacts()
            messagebox.showinfo("Success", "All contacts deleted successfully.")


if __name__ == '__main__':
    root = tk.Tk()
    app = ContactManager(root)
    root.mainloop()
