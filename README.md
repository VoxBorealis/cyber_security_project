# Cyber Security Base 2022 - Course Project I

Small project created as a part of https://cybersecuritybase.mooc.fi/. Assignment was to create a web app with 5 flaws from [OWASP Top 10 Security Risks](https://owasp.org/www-project-top-ten/)

To run the project, clone the files and run the following command (you may need to write 'python3' insted of 'python':

````
python manage.py runserver
````

In case the database is not working properly, run the following aswell.
````
python manage.py makemigrations
python manage.py migrate
````

The application should now be running at http://127.0.0.1:8000/


## FLAW 1: SQL Injection 

https://github.com/VoxBorealis/cyber_security_project/blob/main/todo/views.py#L53

The search_tasks view is flawed because it enables the user to perform a SQL Attack.
Here I am using the Django 'connection' library that allows me to perform raw SQL queries.
This in and of itself is not a flaw, but the way it's used, is.
The way it's set up at the moment would allow the user to input e.g "DOESNOTEXIST' UNION SELECT password FROM todo_user WHERE username = 'admin' --",
which would return the password of any user (such as an admin account).

There are multiple ways to fix this. The obvious fix is, that instead of using raw SQL, we would use the Django model functions, like I've used in other views. If, however, we wanted to use raw SQL, we need to remove the quotes around the %s placeholders. This will prevent the user from formatting the input such that the server reads it as part of the query.


## FLAW 2: CSRF

https://github.com/VoxBorealis/cyber_security_project/blob/main/todo/views.py#L8

The location of this flaw is not pinpointable to a single location, however on line 8 we exempt this view from forcing us to use csrf protection. If we remove that line of code, Django will forbid the page from loading, because we haven't implemented csrf protection. Therefore the actual flaw is at https://github.com/VoxBorealis/cyber_security_project/blob/main/todo/templates/todo/index.html#L38.

We have forgotten to include a csrf token, which is essentially a cookie that confirms that the form was submitted from it's appropriate place. Django enables us just include {% csrf_token %} line of code in the form and it takes care of the rest.

An example of this can be found at https://github.com/VoxBorealis/cyber_security_project/blob/main/todo/templates/todo/index.html#L12



## FLAW 3: Broken Access Control

https://github.com/VoxBorealis/cyber_security_project/blob/main/todo/views.py#L34

OWASP describes Broken Access Control as "Access control enforces policy such that users cannot act outside of their intended permissions. Failures typically lead to unauthorized information disclosure, modification, or destruction of all data or performing a business function outside the user's limits".

The flaw in my task view is that it doesn't check that the user is the owner of the task.
This allows any user to to see anyone's task by modifying the URL from the browser.

The fix for this is quite simple, if the task owner's id is not the same as the user's id, we raise a 403 forbidden error. The fix is also shown in the commented code here: https://github.com/VoxBorealis/cyber_security_project/blob/main/todo/views.py#L36



## FLAW 4: Cryptographic Failures

https://github.com/VoxBorealis/cyber_security_project/blob/main/todo/views.py#L65

In the 'register' function, we take the raw username and password entered by the user and save it to the database as is. This is a major security flaw, because if someone were to gain access to the database, all of the user's passwords and data would be abusable. 

There are multiple ways to fix the flaw in this case; easiest and smartest solution would be to use Django's built-in User database model and authentication system. That would fix many of the security flaws listed in the OWASP top 10. If we wanted to fix it by ourselves, we could use "werkzeug.security" library in python to generate a hashed value of the passwords before saving them to the database. This way the actual password is not stored in the database, but rather, a hash value is. This way, when the user attempts to log in using their credentials, the password they enter in the log in form is hashed and compared to the value stored in
the database. Hashing algorithms are one-way programs, which means that even if you know the algorithm and the result value, you can't decrypt the value to it's original value.



## FLAW 5: Identification and Authentication Failures

The OWASP description of Identification and Authentication Failures is really insightful and worth a read. My program has many of the flaws listed there
but for this example, I'll choose "Permits default, weak, or well-known passwords, such as "Password1" or "admin/admin"".

https://github.com/VoxBorealis/cyber_security_project/blob/main/todo/forms.py#L6

In the registration form, we don't enforce any rules on the type of passwords you can use. This leads to the users using weak passwords leading to their account being at risk.

The way to fix this would be to enforce rules, such as: minimum length, must contain capital letters, numbers or special characters. This will lead to stronger passwords that will be harder to crack or find at leaked password lists that hackers use for malicious purposes.
