# Newegg Price Tracker
### Description
This is the CS50x final project - Newegg Price Tracker

A web-based application to help users track the current price of different products in Newegg's website.

In this web application, flask web framework based on Python is used as it is necessary to use flask-login and flask-sqlalchemy with sqlite3 to manage the user status and user price watches.

Newegg Price Tracker supports the features of multi-user login so every user can create their own price watches from Newegg's Website.

The price tracker gets the product's link from Newegg and then parse the information of the product including name, current price and status of the stock etc.


> The application was built on flask with the intention to use different functions provided in flask.

![Image](https://img.youtube.com/vi/MBgyN2xhngA/maxresdefault.jpg)

### Installation
1. Install and setup [Python](https://www.python.org/) on your computer
https://www.python.org/

2. Install [package installer](https://pypi.org/project/pip/) for Python so you can use pip to install the required packages for this application

3. Install and setup required package to the root file `cs50`
```
pip install -U Flask
pip install beautifulsoup4
pip install flask-login
pip install lxml
pip install html5lib
```

4. Initalization and run the appllication
To intialize the project, run 'main.py' in 'cs50/finalproject/webapp'

5. Test in local
Access the web application: http://127.0.0.1:5000/

### How the Price Track work
#### Registration
User can register account to use the price track application. During the registration, the user need to enter the following fields:
- Username
- Password
- Email

After the registration, the user can access the Home Page of the application.
The user can change the account password after logging in the website.

#### Create Price Watch
User can go to go the `Track` Price Tab to create their price watch.
By copying the URL of product to the input field and entering the target price, click `Start Tracking` to track the product price.
After creating the price watch, the user will be redirect to `Price Watches` to monitor the product's price

#### Price Watches
In the `Price Watches`, the user can view all of the created tracked product.
The information of the tracked product is set to be updated every two minutes
The application displays the dynamic current price and status of the tracked product.
The application calculates the price difference between current price and target price to notify the user whether the current price drops to the target price.
User can change the target price of product and remove the price watch of product on this page.

### Video Demonstration on youtube
https://youtu.be/MBgyN2xhngA

### Technology
- Web Framework: Flask
- Backend Language: Python, HTML, CSS, JavaScript
- Database: Sqlachemy and sqlite3
- Python Library: Beautiful Soup, Flask-Login
- CSS Library: Bootstrap 5
- Web Technique: AJAX

#### Routing
Each route checks if the user is authenticated. It means if correct username and password are provided so the user can use the application.

#### Session
The webapp use `Flask-Login` to provide user session managemenet. It handles the common tasks of logging in, logging out, and remembering your users’ sessions over extended periods of time.

#### Database
Database stores all users and track records. The table like `Users` uses foreign keys to related to tracked products to demonstrate the one-to-many relationship in database.

#### Web Scraping
The webapp uses Beautiful Soup, a Python library for pulling data out of HTML and XML files.
Beautiful Soup supports the HTML parser included in Python’s standard library, but it also supports a number of third-party Python parsers.
The webapp use the lxml’s HTML parser with the advantages of fast speed.

### Documentation
- https://flask-sqlalchemy.palletsprojects.com/en/2.x/
- https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- https://flask-login.readthedocs.io/en/latest/

### About CS50
CS50 is a openware course from Havard University and taught by David J. Malan

Introduction to the intellectual enterprises of computer science and the art of programming. This course teaches students how to think algorithmically and solve problems efficiently. Topics include abstraction, algorithms, data structures, encapsulation, resource management, security, and software engineering. Languages include C, Python, and SQL plus students’ choice of: HTML, CSS, and JavaScript (for web development).

Thank you for CS50

