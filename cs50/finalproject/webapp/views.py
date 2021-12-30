from flask import Blueprint, flash, redirect, url_for, render_template, request, jsonify, send_file
from requests.models import Response
from sqlalchemy.sql.expression import null
from webapp import db
from .models import Users, Tracks
from flask_login import login_required, current_user, LoginManager
from sqlalchemy import create_engine
from sqlalchemy import text, desc
import requests, re, csv, os
from bs4 import BeautifulSoup


views = Blueprint('views', __name__)
    
@views.route("/", methods=["GET", "POST"])
@login_required
def index():
    """
    username = "Admin456"
    sql = text("SELECT * FROM Users WHERE username =:name")
    result = db.engine.execute(sql, name=username)
    for row in result:
        print(row["email"])
    
    
    sql = text("SELECT * FROM Tracks WHERE user_id = :id ORDER BY date")
    result = db.engine.execute(sql, id=current_user.id)
    
    for row in result:
        print(row)
    """

    # raw sql query for the tracked product by current_user.id
    sql = text("SELECT * FROM Tracks WHERE user_id = :id ORDER BY date DESC LIMIT 3")
    products = db.engine.execute(sql, id=current_user.id)

    # initalize the product list to store dict object
    productlist = []

    for product in products:

        # convert sqlaclehemy keyed tuple to dict
        product = product._asdict()

        # add new key-value pair
        product["currentprice"] = checkprice(product["url"])

        # append dict object to list
        productlist.append(product)
    return render_template("index.html", user=current_user, products=productlist)


@views.route("/track", methods=["GET", "POST"])
@login_required
def track():
    """Insert Newegg's products data"""
    if request.method == "POST":

        productlink = request.form.get("productlink")
        targetprice = request.form.get("targetprice")

        # Ensure the productlink is submitted
        if not productlink:
            flash("Missing product's link", category="error")
            return redirect("/track")


        # Ensure the target price is submitted
        elif not targetprice:
            flash("Missing target price", category="error")
            return redirect("/track")

        else:
            # Get the html text from website
            html_text = requests.get(productlink).text

            # Use lxml parser to scrape information from html text
            soup = BeautifulSoup(html_text, "lxml")

            # Search for the product by CSS class
            productname = soup.find("h1", class_="product-title").text.strip()

            try:
                raw_price = soup.find("div", class_="price-current").text
                # Extract price by regular expression only ASCII digit
                price = float(re.search(r'[0-9,.]+', raw_price).group().replace(",", ""))
            except:
                price = None
            
            # define new track
            new_track = Tracks(user_id=current_user.id ,url=productlink, productname=productname, trackedprice=price, targetprice=targetprice)

            # Insert the track record into database
            db.session.add(new_track)
            db.session.commit()

            flash(f"Create Price Tracking successful!", category="success")

            return redirect("/tracker")

    else:
        return render_template("track.html", user=current_user)


@views.route("/tracker", methods=["GET", "POST"])
@login_required
def tracker():

    """Show the tracker of Newegg's products"""

    """
    products = Tracks.query.filter_by(user_id=current_user.id).order_by(desc(Tracks.date)).all()
    
    for product in products:
        product.currentprice = checkprice(product.url)
        product.status = checkstatus(product.url)
        product.diff = product.currentprice - product.targetprice
    """
    if request.method == "POST":

        if request.form["button"] == "Edit Target Price":

            editid = request.form.get("editid")
            newtargetprice = request.form.get("newtargetprice")

            # ensure the target price is submitted
            if not newtargetprice:
                flash("New Target Price missing.", category="error")
                return redirect("/tracker")
        
            else:
                # edit the selected product's target price
                sql = text("UPDATE TRACKS SET targetprice = :newtargetprice WHERE id = :productid")
                db.engine.execute(sql, productid=editid, newtargetprice=newtargetprice)

                flash(f"Edit target price successful!", category="success")
                return redirect("/tracker")

        elif request.form["button"] == "Remove":

            removeid = request.form.get("removeid")
            # remove the selected product from watchlist
            sql2 = text("DELETE FROM Tracks WHERE id = :productid")
            db.engine.execute(sql2, productid=removeid)

            flash(f"Remove selected item successful!", category="success")
            return redirect("/tracker")
                    
    else:
        # raw sql query for the tracked product by current_user.id
        sql = text("SELECT * FROM Tracks WHERE user_id = :id ORDER BY date DESC LIMIT 20")
        products = db.engine.execute(sql, id=current_user.id)

        # initalize the product list to store dict object
        productlist = []

        for product in products:
            # convert sqlaclehemy keyed tuple to dict
            product = product._asdict()

            # add new key-value pair
            product["currentprice"] = checkprice(product["url"])
            product["status"] = checkstatus(product["url"])

            if not product["currentprice"] == None:
                product["pricediff"] = float(product["currentprice"] - product["targetprice"])
            else:
                product["pricediff"] = None

            # append dict object to list
            productlist.append(product)
           
        return render_template("tracker.html", user=current_user, products=productlist)


@views.route("/getprice")
def ajax():
    """ Return current user JSON for ajax request """
     # raw sql query for the tracked product by current_user.id
    sql = text("SELECT * FROM Tracks WHERE user_id = :id LIMIT 20")
    products = db.engine.execute(sql, id=current_user.id)

    # initalize the product list to store dict object
    productlist = []

    for product in products:
        # convert sqlaclehemy keyed tuple to dict
        product = product._asdict()
        try:
            product["currentprice"] = checkprice(product["url"])
        
        except:
            product["currentprice"] = None

        try:
            product["pricediff"] = float(product["currentprice"] - product["targetprice"])
        except KeyError:
            product["pricediff"] = None
            print("Current price is unknown.")
        except:
            product["pricediff"] = None
            print("current price is unknown.")

        product["status"] = checkstatus(product["url"])

        # append dict object to list
        productlist.append(product)

    return jsonify(productlist)


@views.route("/cleartrack")
@login_required
def clear():
    Tracks.query.delete()
    db.session.commit()
    return redirect(url_for("views.index")) 

@views.route("/download")
@login_required
def download():
    sql = text("SELECT productname, targetprice, trackedprice, url FROM Tracks WHERE user_id = :id ORDER BY date DESC")
    products = db.engine.execute(sql, id=current_user.id)

    with open("pricewatch.csv", "w") as csvfile:
        writer = csv.writer(csvfile, lineterminator='\n')
        writer.writerow(["Name", "Target Price", "Tracked Price", "URL"])

        for product in products:
            writer.writerow(product)
    
    filename = os.path.join("/Users/sn023", 'cs50', 'pricewatch.csv')
    return send_file(filename
                     ,as_attachment=True)

def checkprice(url):
    # Get the html text from website
    session = requests.Session()
    html_text = session.get(url).text
    #html_text = requests.get(url).text

    # Use lxml parser to scrape information from html text
    soup = BeautifulSoup(html_text, "lxml")

    try:
        raw_price = soup.find("div", class_="price-current").text
        # Extract price by regular expression only ASCII digit
        price = float(re.search(r'[0-9,.]+', raw_price).group().replace(",", ""))
    except:
        price = None
    
    return price

def checkstatus(url):
    # Get the html text from website
    session = requests.Session()
    html_text = session.get(url).text

    # Use lxml parser to scrape information from html text
    soup = BeautifulSoup(html_text, "lxml")

    try:
         # Parse for status
        status = soup.find("div", class_="product-inventory").text.strip().replace(".","")
    except:
        status = "Not available"
    
    return status




        
