import sqlite3

db = sqlite3.connect(':memory:')
#db = sqlite3.connect('data/mydb')

cursor = db.cursor()
name1 = 'Andres'
phone1 = '3366858'
email1 = 'user@example.com'
password1 = '12345'

name2 = 'John'
phone2 = '5557241'
email2 = 'johndoe@example.com'
password2 = 'abcdef'

cursor.execute('''
    CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT,
                       phone TEXT, email TEXT unique, password TEXT)
''')

cursor.execute('''INSERT INTO users(name, phone, email, password)
                  VALUES(?,?,?,?)''', (name1, phone1, email1, password1))
print('First user inserted' + '\n')

cursor.execute('''INSERT INTO users(name, phone, email, password)
                  VALUES(?,?,?,?)''', (name2, phone2, email2, password2))
print('Second user inserted' + '\n')

db.commit()

cursor.execute('''SELECT name, email, phone, password FROM users''')
user1 = cursor.fetchone()
print(user1[0] + '\n')
all_rows = cursor.fetchall()
for row in all_rows:
    print('{0} : {1}, {2}, {3}'.format(row[0], row[1], row[2], row[3]) + '\n')

user_id = 1
cursor.execute('''SELECT name, email, phone, password FROM users WHERE id=?''', (user_id,))
user = cursor.fetchone()
print(user)

newphone = '3113093164'
userid = 1
cursor.execute('''UPDATE users SET phone = ? WHERE id = ? ''', (newphone, userid))
db.commit()

cursor.execute('''SELECT name, email, phone, password FROM users WHERE id = ? ''', (userid,))
userchanged = cursor.fetchone()
print(userchanged)

delete_userid = 2
cursor.execute('''DELETE FROM users WHERE  id = ? ''', (delete_userid,))
db.commit()
# Roll back the change
# db.rollback()

cursor.execute('''SELECT name, email, phone, password FROM users WHERE id = ? ''', (delete_userid,))
userchanged = cursor.fetchone()
print(userchanged)

id = cursor.lastrowid
print('Last row id: %d' % id + '\n')

print(user1[2])

db.close()
