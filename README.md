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
* Github - for version control
* Heroku - for deployment


## Logic Flow

### Login in flowchart
~~~mermaid
graph TD
a(Login Screen)
b(username and password entry)
c(login selected)
d(create account selected)
e{{user known}}
f{{password hash matches}}
g(home screen)
h{{user known}}
i(create user)

a-->b-->c & d
c --> e
e --yes--> f --yes--> g
e & f -. no .-> b
d-->h
h -.yes.-> b
h --no--> i --> g
g --> c1(create login) & vl(view logins) & lo(logout)
lo -.-> a
~~~


### Create Entry flowchart
~~~mermaid
graph TD
hs(home screen)-->cl(create login screen)
cl-->pl(password length changed)-->g(generate new password)-.->cl
cl-->o1(password options changed)-->g
cl-->ok(OK selected)
ok-->nv{{name is valid}}--yes-->ar
nv-.no.->cl
ar(add record to database)-.->hs
cl-->cn(cancel selected)-.->hs
~~~


### View entries flowchart
~~~mermaid
graph TD
hs(home screen)-->vl(view logins)

vl-->ok(OK Selected)-.->hs
vl-->nc(name filter changed)-->up(update list)-.->vl
vl-->is(item selected)-->sd(show details)-->wt(wait for input)-.->vl
~~~


