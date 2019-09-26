#!/usr/bin/env python3
"""
    * CLI Diary app
"""


from collections import OrderedDict
import datetime
import sys
import os

import peewee as pw


DB = pw.SqliteDatabase('diary.db')


class Entry(pw.Model):
    content = pw.TextField()
    timestamp = pw.DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DB


def initialize():
    """Create the database and the table if they don't exist."""
    DB.connect()
    DB.create_tables([Entry], safe=True)


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def show_menu():
    """Shows users menu."""
    choice = None

    while choice != 'q':
        clear()
        print("Enter 'q' to quit.")
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()

        if choice in menu:
            clear()
            menu[choice]()


def add_entry():
    """Add a new entry."""
    print("Enter your entry. Press 'Ctrl+D' when finished.")
    data = sys.stdin.read().strip()

    if data:
        if input('Save entry? [y/n] ').lower() != 'n':
            Entry.create(content=data)
            print('Saved successfully!')


def view_entries(search_query=None):
    """View previous entries."""
    entries = Entry.select().order_by(Entry.timestamp.desc())

    if search_query:
        entries = entries.where(Entry.content.contains(search_query))

    for entry in entries:
        timestamp = entry.timestamp.strftime('%A %B %d, %Y, %I:%M%p')
        clear()
        print(timestamp)
        print('=' * len(timestamp))
        print(entry.content)
        print('\n\n' + '=' * len(timestamp))
        print('n) next entry')
        print('d) delete entry')
        print('q) return to main menu')

        next_action = input('Action: [n/d/q] ').lower().strip()
        if next_action == 'q':
            break
        elif next_action == 'd':
            delete_entry(entry)


def search_entries():
    """Search entries."""
    view_entries(input('Search query: '))


def delete_entry(entry):
    """Delete an entry."""
    if input('Are you sure? [y/n] ').lower().strip() == 'y':
        print('Shooh! Entry deleted.')
        entry.delete_instance()


menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entries),
    ('s', search_entries),
])


if __name__ == '__main__':
    initialize()
    show_menu()
