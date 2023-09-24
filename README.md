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

### create login flowchart
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

## Deployment
The app itself is deployed on Heroku, using a github template from Code Institute to provide the terminal emulator.  

The database is deployed on AWS EC2, using a docker container running with an ubuntu host.  The database is a PostgreSQL database.

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

