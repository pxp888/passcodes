# Passcodes - simple password manager

[Live Link](https://passcodes-993cec8b97da.herokuapp.com/)


## Description
Passcodes is a very simple password manager written in Python. Each record consists of a name, username, password, and URL. 

## Features
* __Secure login__
    * User accounts are created and associated with passwords that are hashed and salted.  Plaintext passwords are not stored.
* __Create Login records__
    * Users can create records for each login they want to store.  Each record consists of a name, username, password, and URL.
* __Random Password generation__
    * Users can generate a random password of a specified length.  
    * Options exist to include numbers or special symbols in the password.
* __Safe password storage__
    * Passwords are encrypted using the Fernet encryption scheme.  The encryption key is the users main password, which is not stored in the database.  
* __Dynamic Search by name__
    * Users can search for records by name. The search is dynamic, so results are updated as the user types.


## Cryptographic Security
### Primary User Passwords
The primary user passwords, or master passwords are not stored in the database.  Each password is assigned a salt value, and the password plus the salt value are hashed using the SHA256 algorithm.  

The salt value is stored in the database, and the hashed password is stored in the database.  

When a user attempts to login, the salt value is retrieved from the database, and the password entered by the user is hashed using the same salt value.  

If the hashed password matches the hashed password in the database, the user is logged in.  If the hashed passwords do not match, the user is not logged in.

### Login Passwords
The passwords for each login record are encrypted using the Fernet encryption scheme.  The encryption key is the users master password.  

The master password is not stored in the database, so the login passwords cannot be decrypted without the master password.






## Interface Flowchart

There are five main forms that the user interacts with.  

### Overall flowchart
~~~mermaid
graph TD
lg[[login form]]
hs[[home screen]]
cl[[create login form]]
vl[[view logins form]]
vd[[view details]]

lg-->hs<-->cl & vl
hs-.logout.->lg
vl<-->vd
~~~

### Login flowchart
~~~mermaid
graph TD
lg[[login form]]
de(username and password entry)
ls(Login)
cs(Create account )
uk1{{username known}}
uk2{{username known}}
pw1{{password hash correct}}
hs[[home screen]]
ad[(add user to database)]
pv{{password valid}}

lg-->de & ls & cs
ls-->uk1-->|yes|pw1-->|yes|hs
pw1-.->|no|lg
uk1-.->|no|lg
cs-->uk2-->|no|pv-->|yes|ad-->hs
pv-.->|no|lg 
uk2-.->|yes|lg
~~~

There are two methods of getting from the first login screen to the home screen.  One is to create a new account, and the other is to login to an existing account.  The flowchart shows both methods.

To create a new account, the user enters a username and password, and clicks the create account button.  The username is checked to make sure it is not already in use.  If it is not in use, the password is hashed and salted, and the username and hashed password are stored in the database.  The user is then logged in.

To login to an existing account, the user enters a username and password, and clicks the login button.  The username is checked to make sure it exists in the database.  If it does, the password is hashed and salted, and compared to the hashed password in the database.  If the passwords match, the user is logged in.


### create login records flowchart
~~~mermaid
graph TD

hs[[home screen]]
cl[[create login form]]
gp(generate random password)

ok(OK selected)
nv{{name is valid}}
add[(add login to database)]

op1(password options changed)

hs<-->cl
cl-->ok & op1 

ok-->nv
nv-.->|no|cl
nv-->|yes|add-.->hs
op1-->gp-.->cl
~~~

The form to create new login records has multiple fields.  The name field is used to identify and search for the record.  The username, password, and URL fields are used to store the login information.  

The only required field is the name field.  Blank entries are allowed for all others, but the name field must be valid for the record to be saved.  

Multiple records can exist with the same name. 

The suggested password for each record is automatically generated.  If the user does not like the suggested password, they can click the generate password button to generate a new password.  The user can also change the length of the password, and choose to include numbers or special symbols in the password.

The password field itself is editable, so the user may alter the suggested password if they wish.


### view logins flowchart

~~~mermaid
graph TD
hs[[home screen]]
vl[[view logins form]]

nf(names filtered)
hs<-->vl
vl-->nf-->ul1(update list)-.->vl

vl<-->ns(name selected)-->sd[[view details]]
sd-->wt(wait for input)-.->vl
~~~

The form for viewing records has just two elements.  The first is a name filter field.  As the user types in the name filter field, the list of records is filtered to only show records that contain the text in the name filter field.

This main list shows only one entry for each name.  If multiple records with the same name exist, only the last one entered is shown.  

The user can then select which record he wants to see from the main list.  The record details are then displayed in a separate screen, along with the passwords.  The user can then copy the username or password to the clipboard. 

On this screen all entries with the same name are shown, so the user can see all the records with the same name. This means a user can see a history of records for entries with the same name.  

There is no interaction on this screen, it just waits for the user to press a key to return to the main list.

__Note__- _the terminal emulator used to host the app on Heroku does not support shift-tab to move focus backwards.  There are three widgets on this form that accept focus, the name filter, the list itself, and the OK button at the bottom that returns the user to the home screen._

_This means that when the main list has focus it cannot return to the name filter field.  This can be fixed by overwriting the python curses code that handles keypresses, but this has not been done yet.  The user can still use the mouse to click on the name filter field to return focus to it._

## Technologies and Frameworks used
* VSCode - IDE used for development
* Python
    * npyscreen - for creating the terminal user interface (TUI)
    * cryptography - for encrypting and decrypting passwords
    * psycopg2 - for connecting to the database

* Github - for version control
* Heroku - for deployment of the app itself
* PostgreSQL - for database storage
* Docker - containerization of PostgreSQL database
* AWS EC2 - for hosting the database container

## Deployment
The app itself is deployed on Heroku, using a github template from Code Institute to provide the terminal emulator.

The database is PostgreSQL running in a Docker container on an AWS EC2 instance with an ubuntu host instance.

The database is accessed by the app using the psycopg2 library.  The database URL is stored in an environment variable on Heroku.

## Pending Improvements
* __move database to Heroku__
    * I happened to have an AWS EC2 instance running, so I used that to host the database.  I would like to move the database to Heroku.

* __move database password to environment variable__
    * The database password is currently stored in the code.  I would like to move it to an environment variable.

* __add ability to edit or delete login records__
    * Currently there is no method of editing or deleting login records.  I would like to add this functionality.  There are multiple entries allowed for each login name, so this does not hurt the functionality of the app, but it would be cleaner to allow editing and deleting of records.

* __add ability to edit or delete user accounts__
    * There is no method of editing or deleting user accounts.  This is a functional issue in the case that a user wants to change their master password, or if they have lost their master password.


