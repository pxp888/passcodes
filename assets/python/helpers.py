import os
import hashlib
import random
import base64
import psycopg2

from cryptography.fernet import Fernet

# CRYPTOGRAPHY FUNCTIONS
# These are defined here to make it easier to change the encryption methods later


def hash(plaintext):
    # this is a hash function
    return hashlib.sha256(plaintext.encode()).digest()


def encrypt(plaintext, key):
    # this is an encryption function
    key = base64.b64encode(hash(key))
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(plaintext.encode())
    return cipher_text.decode()


def decrypt(ciphertext, key):
    # this is a decryption function
    key = base64.b64encode(hash(key))
    cipher_suite = Fernet(key)
    plain_text = cipher_suite.decrypt(ciphertext.encode())
    return plain_text.decode()


# DATABASE FUNCTIONS
# These are defined here to make it easier to change the database later.  
# The global variable db_connection is used to store the database connection, so it can be re-used.
# The database connection details are stored in environment variables, DB_PW and DB_IP for the password and IP address respectively.

db_connection = None


def getDBConnection():
    # This is a helper function used by the database calls below to get
    # a database connection.
    # This enables the same connection to be used for multiple calls,
    # and re-establishes the connection if it is lost.
    # The database connection details are stored in environment variables.

    db_pw = os.environ.get('DB_PW')
    db_ip = os.environ.get('DB_IP')
    if db_ip is None:
        db_ip = "localhost"

    global db_connection
    if db_connection is None or db_connection.closed != 0:
        try:
            db_connection = psycopg2.connect(
                host=db_ip,
                database="postgres",
                user="postgres",
                password=db_pw
            )
        except psycopg2.OperationalError:
            # if the connection times out, re-establish it
            db_connection = psycopg2.connect(
                host=db_ip,
                database="postgres",
                user="postgres",
                password=db_pw
            )
    return db_connection


def setupStorage():
    # create database tables if they don't exist.  This should only be called once at the start of the application.
    conn = getDBConnection()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS passcodes
        (ID SERIAL PRIMARY KEY,
        OWNER TEXT,
        NAME TEXT,
        USERNAME TEXT,
        PASSWORD TEXT,
        URL TEXT);''')
    cur.execute('''CREATE TABLE IF NOT EXISTS users
        (ID SERIAL PRIMARY KEY,
        USERNAME TEXT,
        SALT TEXT,
        PASSWORD TEXT);''')
    conn.commit()
    cur.close()


def getUserLoginData(username):
    # gets login data from the database for a given username.
    conn = getDBConnection()
    cur = conn.cursor()
    cur.execute("SELECT USERNAME, SALT, PASSWORD FROM users WHERE USERNAME = %s ORDER BY ID DESC", (username,))
    result = cur.fetchone()
    cur.close()

    if result is None:
        return None
    else:
        return result


def saveUserLoginData(username, password):
    # saves login data to the database
    salt = str(random.randint(1000000000000000, 9999999999999999))
    passwordHash = str(hash(password + salt))

    conn = getDBConnection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (USERNAME, SALT, PASSWORD) VALUES (%s, %s, %s)", (username, salt, passwordHash))
    conn.commit()
    cur.close()


def getUserData(owner, masterPassword):
    # gets records for a user from the database
    conn = getDBConnection()
    cur = conn.cursor()
    cur.execute("SELECT NAME, USERNAME, PASSWORD, URL FROM passcodes WHERE OWNER = %s", (owner,))
    records = cur.fetchall()
    cur.close()

    for i in range(len(records)):
        name, username, password, url = records[i]
        records[i] = (name, username, decrypt(password, masterPassword), url)
    return records


def saveUserData(owner, name, username, password, url, masterPassword):
    # saves records for a user to the database
    password = encrypt(password, masterPassword)

    conn = getDBConnection()
    cur = conn.cursor()
    cur.execute("INSERT INTO passcodes (OWNER, NAME, USERNAME, PASSWORD, URL) VALUES (%s, %s, %s, %s, %s)", (owner, name, username, password, url))
    conn.commit()
    cur.close()


setupStorage()
