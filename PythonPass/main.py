from cryptography.fernet import Fernet  # import cryptography
from connection import connection
import os
key = ''


# This item is for the contents of a given site.
class Item:
    def __init__(self, site, username, password):
        self.site = site  # Each site should have a unique name
        self.username = username  # Site username/email
        self.password = password  # Site password


# Saves an item to the database
def save(tosave):
    mydb = connection()
    mycursor = mydb.cursor()

    sql = "INSERT INTO data (site, username, password) VALUES (%s, %s, %s)"
    encrypted = encrypt(tosave.password)
    val = (tosave.site, tosave.username, encrypted)
    mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "record inserted.")


# Encrypts a string
def encrypt(string):
    cipher_suite = Fernet(key)
    ciphered_text = cipher_suite.encrypt(bytes(string, 'UTF-8'))   # required to be bytes
    return ciphered_text


# Reads the Database
def read_dba(query):
    mydb = connection()

    mycursor = mydb.cursor()

    newQuery = "SELECT * FROM data WHERE " + query
    print("\n---RESULTS---")

    mycursor.execute(newQuery)

    myresult = mycursor.fetchall()
    for x in myresult:
        site, username, password = x
        password = decrypt_this(password)
        newPassword = str(password)
        newPassword = newPassword.replace('b\'', '')
        newPassword = newPassword.replace('\'', '')

        print("Site: \"" + site + "\" Username: \"" + username + "\" Password: " + newPassword + "")


# Decrypts a string
def decrypt_this(todecrypt):
    cipher_suite = Fernet(key)
    unciphered_text = (cipher_suite.decrypt(bytes(todecrypt, 'utf-8')))
    return unciphered_text


# Gets the key from the text file
def get_key():
    f = open("key.txt", 'r')
    temp = f.read()
    return temp


# Main program
def main():
    os.system('cls')
    global key
    temp = str(get_key())
    key = bytes(temp, 'utf-8')
    choice = input("\nWhat would you like to do? \n1-> Add\n2-> Search/View \n3-> Edit Records \n4-> Exit \n")
    if choice == '1':
        site = input("Input the service for the record: ")
        username = input("Input the username for the service: ")
        password = input("Input the password for the service: ")
        toadd = Item(site, username, password)
        save(toadd)
        main()
    elif choice == '2':
        get_choice()
    elif choice == '3':
        edit()
    elif choice == '4':
       print("Exiting System")
       quit()
    else:
        print("That was not an option")
        main()


# Gets the choice etc
def get_choice():
    choice = input("Type the service you want to search for or use % as a wild card.\n" +
                   "Typing \'%\' on its own will return all results: ")
    if choice != "":
        read_dba("site LIKE \"%" + choice + "%\"")
        input("\nPress Enter to return")
        main()
    else:
        read_dba("site LIKE \"%\"")
        input("\nPress Enter to return")
        main()


# Allows the editing of records
def edit():
    mydb = connection()

    mycursor = mydb.cursor()

    newQuery = "SELECT * FROM data "
    print("\n---RESULTS---")

    mycursor.execute(newQuery)

    myresult = mycursor.fetchall()
    i = 0
    for x in myresult:
        site, username, password = x
        password = decrypt_this(password)
        newPassword = str(password)
        newPassword = newPassword.replace('b\'', '')
        newPassword = newPassword.replace('\'', '')

        print(str(i) + " - Site: \"" + site + "\" Username: \"" + username + "\" Password: " + newPassword + "")
        i = i+1
    choice = input("\nPlease select a record to edit or q to quit: ")
    if choice == 'q':
        main()
    else:
        flag = False
        os.system('cls')
        i=0
        for x in myresult:
            site, username, password = x
            password = decrypt_this(password)
            newPassword = str(password)
            newPassword = newPassword.replace('b\'', '')
            newPassword = newPassword.replace('\'', '')
            if str(i) == choice:
                print("Site: \"" + site + "\" Username: \"" + username + "\" Password: " + newPassword + "")
                newsite = input("Please input the new site name or leave blank for no change: ")
                if newsite == "":
                    newsite = site
                newusername = input("Please input the new username or leave blank for no change: ")
                if newusername == "":
                    newusername = username
                newpass = input("Please input the new password or leave blank for no change: ")
                if newpass == "":
                    newpass = password
                else:
                    newpass = encrypt(newpass)
                    print(newsite)
                    print(newpass)
                    print(newusername)
                mydb2 = connection()
                newpass = str(newpass)
                newpass = newpass.replace('b\'', '\'')

                mycursor2 = mydb2.cursor()
                newQuery2 = "UPDATE data SET site = '"+newsite+"', username = '"+newusername+"', password = "+newpass+" WHERE data.site = '"+site+"' "
                mycursor2.execute(newQuery2)
                mydb2.commit()
                mydb.commit()
                flag = True
                print("Successfully Updated")
                main()
            i = i+1
        if flag == False or i > 100:
            print("Record not found")
            main()





main()

