from flask import Blueprint, request, render_template, redirect, url_for, flash
from db import mysql
from music21 import note, stream
#import composition
import xml.etree.ElementTree as ET

archivo_xml = ET.parse('my_melody_IA.musicxml')

raiz = archivo_xml.getroot()

print(raiz)

for hijo in raiz:
    print(hijo.text)

import time
#MIDI
s = stream.Stream()

contacts = Blueprint('contacts', __name__, template_folder='app/templates')


@contacts.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', contacts=data)


@contacts.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO contacts (fullname, phone, email) VALUES (%s,%s,%s)", (fullname, phone, email))
            mysql.connection.commit()
            flash('Contact Added successfully')
            return redirect(url_for('contacts.Index'))
        except Exception as e:
            flash(e.args[1])
            return redirect(url_for('contacts.Index'))


@contacts.route('/edit/<id>', methods=['POST', 'GET'])
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-contact.html', contact=data[0])


@contacts.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts
            SET fullname = %s,
                email = %s,
                phone = %s
            WHERE id = %s
        """, (fullname, email, phone, id))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('contacts.Index'))


@contacts.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('contacts.Index'))


@contacts.route('/gen', methods=['GET'])
def Indexxz():
    
    n1 = note.Note('E', quarterLength = 1)
    n2 = note.Note('E', quarterLength = 1)
    n3 = note.Note('B', quarterLength = 1)
    n4 = note.Note('B', quarterLength = 1)
    n5 = note.Note('C#5', quarterLength = 1)
    n6 = note.Note('C#5', quarterLength = 1)
    n7 = note.Note('B', quarterLength = 2)
    n8 = note.Note('A', quarterLength = 1)
    n9 = note.Note('A', quarterLength = 1)
    n10 = note.Note('G#', quarterLength = 1)
    n11 = note.Note('G#', quarterLength = 1)
    n12 = note.Note('F#', quarterLength = 1)
    n13 = note.Note('F#', quarterLength = 1)
    n14 = note.Note('E', quarterLength = 2)
    s.append([n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14])
    s.show()
    s.write('midi', fp='my_melody.midi')
    #s.write('musicxml.pdf', fp='my_melody_IA.pdf')
    return render_template('index.html')