# Passcodes - simple password manager

[Live Link](https://passcodes-993cec8b97da.herokuapp.com/)


## Description
Passcodes is a very simple password manager written in Python. Each record consists of a name, username, password, and URL. 

## Features
* Secure login 
    * User accounts are created and associated with passwords that are hashed and salted.  Plaintext passwords are never stored.  
* Create Login records
    * Users can create records for each login they want to store.  Each record consists of a name, username, password, and URL.
* Random Password generation
    * Users can generate a random password of a specified length.  
    * Options exist to include numbers or special symbols in the password.
* Safe password storage
    * Passwords are encrypted using the Fernet encryption scheme.  The encryption key is the users main password, which is not stored in the database.  
* Dynamic Search
    * Users can search for records by name. The search is dynamic, so results are updated as the user types.
* Copy mode 
    * The filtered records can be printed to screen in a way that enables users to copy information they may want.  This is useful for copying passwords to the clipboard.


## Technologies and Frameworks used
* VSCode - IDE used for development
* Python
    * npyscreen - for creating the terminal user interface (TUI)
    * cryptography - for encrypting and decrypting passwords
* Github - for version control
* Heroku - for deployment

