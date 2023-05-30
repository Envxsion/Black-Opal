import csv
import random
import string

# Generate random usernames and passwords
usernames = []
passwords = []
for i in range(4000):
    username = ''.join(random.choices(string.ascii_uppercase, k=3)) + ''.join(random.choices(string.digits, k=4))
    password = ''.join(random.choices(string.digits, k=12))
    usernames.append(username)
    passwords.append(password)

# Save usernames and passwords to CSV file
with open('datastore.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Username', 'Password'])
    for i in range(len(usernames)):
        writer.writerow([usernames[i], passwords[i]])