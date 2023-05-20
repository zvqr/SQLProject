from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"


def create_table():
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS contacts
                 (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, email TEXT)''')
    conn.commit()
    conn.close()


create_table()


@app.route('/')
def index():
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute("SELECT * FROM contacts")
    contacts = c.fetchall()
    conn.close()
    return render_template('index.html',
                           contacts=[{'id': contact[0], 'name': contact[1], 'phone': contact[2], 'email': contact[3]}
                                     for contact in contacts])


@app.route('/add_contact', methods=['POST'])
def add_contact():
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']

    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
    conn.commit()
    conn.close()

    flash("Contact added successfully.")
    return redirect(url_for('index'))


@app.route('/delete_contact/<int:contact_id>', methods=['GET'])
def delete_contact(contact_id):
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    conn.commit()
    conn.close()

    flash("Contact deleted successfully.")
    return redirect(url_for('index'))


@app.route('/delete_all_contacts', methods=['GET'])
def delete_all_contacts():
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute("DELETE FROM contacts")
    conn.commit()
    conn.close()

    flash("All contacts deleted successfully.")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
