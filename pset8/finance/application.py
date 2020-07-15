import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    user_id = session['user_id']
    db_data = db.execute("SELECT users.cash, wallet.amount, wallet.symbol FROM users JOIN wallet ON "
                         "wallet.id=users.id WHERE users.id = :user_id", user_id=user_id)
    current_price = {}
    current_amount = {}
    # Gain all actual info for shares we own
    for stock in db_data:
        current_price[stock['symbol']] = lookup(stock['symbol'])['price']  # create dict with all symbol = actual price
        current_amount[stock['symbol']] = stock['amount']  # create dict with all symbol = amount
    if not db_data:
        db_data = db.execute("SELECT cash FROM users WHERE users.id = :user_id", user_id=user_id)
        cash = db_data[0]['cash']
        return render_template("index.html", cash=cash, total_cash=cash)
    cash = db_data[0]['cash']

    # create new var to count all our value in usd
    total_cash = cash
    for symbol, amount in current_price.items():
        total_cash += amount * current_amount[symbol]
    # return str(current_amount)
    return render_template("index.html", current_price=current_price, cash=cash, db_data=db_data, total_cash=total_cash)

@app.route("/cash", methods=["GET", "POST"])
@login_required
def cash():

    user_id = session['user_id']

    if request.method == "POST":
        try:
            mon = int(request.form.get("cash"))
        except:
            return apology("Type digits please")
        if mon < 1:
            return apology("You can only add money")

        db.execute("UPDATE users SET cash = cash + :mon WHERE id = :user_id", user_id=user_id,
                   mon = mon)

        return redirect("/")
    else:

        return render_template("cash.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    user_id = session['user_id']
    if request.method == "POST":
        symbol = request.form.get("symbol")
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("Type digits please")
        if shares < 1:
            return apology("Please enter amout of shares you want to buy")

        if not symbol:
            return apology("You need type 4 symbol of some stock", 400)
        # The power of helpers I summon you!
        return_data = lookup(symbol)

        if not return_data:
            return apology("gess better or google right ticker symbols")

        price = float(return_data['price'])
        symbol = return_data['symbol']  # just in case change symbol from user input into symbol from the site

        cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=user_id)
        cash = float(cash[0]['cash'])  # get from db only sum
        all_price = price * shares
        if all_price > cash:
            return apology("You need {}usd, and you have now {}usd".format(all_price, cash))
        time = datetime.now()
        # make a history
        db.execute(
            "INSERT INTO history (id, symbol, amount, time, price, state) VALUES(:id, :symbol, :amount, :time, :price, :state)",
            id=user_id, symbol=symbol, time=time, amount=shares, price=price, state="buy")

        try:
            rows = db.execute("SELECT * FROM wallet WHERE id = :id AND symbol = :symbol",
                              id=user_id, symbol=symbol)
        except:
            return apology(" something wrong with db", 403)  # this try/except is usseles

        # Ensure wallet is not empy
        if len(rows) == 1:  # or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            # update wallet
            db.execute("UPDATE wallet SET amount = amount+:shares WHERE id = :id AND symbol = :symbol", id=user_id,
                       symbol=symbol, shares=shares)
        else:
            # make new wallet
            db.execute("INSERT INTO wallet (id, symbol, amount) VALUES(:id, :symbol, :amount)", id=user_id,
                       symbol=symbol, amount=shares)

        # update cash
        db.execute("UPDATE users SET cash = :all_price WHERE id = :user_id", user_id=user_id,
                   all_price=cash - all_price)

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session['user_id']
    history = db.execute("SELECT * FROM history WHERE id=:id", id=user_id)

    return render_template("history.html", title='History', history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("You need type 4 symbol of some stock", 400)
        # The power of helpers I summon you!
        price = lookup(symbol)

        if not price:
            return apology("gess better or google right ticker symbols")
        price_usd = usd(price['price'])

        return render_template("quoted.html", symbol=symbol, price_usd=price_usd)


    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists
        if len(rows) == 1:  # or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("username allready exist", 403)

        # Ensure password and check are the same
        if request.form.get("password") != request.form.get("check_password"):
            return apology("password's must be the same", 403)
        db.execute('INSERT INTO users (username, hash, cash) VALUES(:username,:phash, :cash)',
                   username=request.form.get("username"), phash=generate_password_hash(request.form.get("password")),
                   cash="10000")  # TODO make insertion
        # Remember which user has logged in
        # session["user_id"] = rows[0]["id"]  #autologin after register maybe?

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/change", methods=["GET", "POST"])
@login_required
def change():

    user_id = session['user_id']

    if request.method == "POST":

        old_pass = db.execute("SELECT hash FROM users WHERE id = :user_id", user_id = user_id)
        if not check_password_hash(old_pass[0]["hash"], request.form.get("password")):
            return apology("type right old password", 403)
        # Ensure new password and check are the same
        if request.form.get("new_password") != request.form.get("check_password"):
            return apology("password's must be the same", 403)
        db.execute("UPDATE users SET hash = :phash WHERE id = :user_id", user_id = user_id, phash = generate_password_hash(request.form.get("new_password")))

        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("change.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    user_id = session['user_id']
    my_shares = db.execute("SELECT symbol, amount FROM wallet WHERE id = :user_id", user_id=user_id)
    if request.method == "POST":
        symbol = request.form.get("symbol")
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("Type digits please")
        if shares < 1:
            return apology("Please enter amout of shares you want to sell")

        if not symbol:
            return apology("You need type 4 symbol of some stock", 400)
        # The power of helpers I summon you!
        return_data = lookup(symbol)

        if not return_data:
            return apology("gess better or google right ticker symbols")

        price = float(return_data['price'])
        symbol = return_data['symbol']  # just in case change symbol from user input into symbol from the site

        cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=user_id)
        cash = float(cash[0]['cash'])  # get from db only sum
        wallet = db.execute("SELECT amount FROM wallet WHERE id = :user_id AND symbol = :symbol", user_id=user_id,
                            symbol=symbol)
        if not wallet:
            return apology("You dont have any of {}".format(symbol), 403)
        wallet = int(wallet[0]['amount'])
        if shares > wallet:
            return apology("You have only {}".format(wallet), 403)
        time = datetime.now()
        # TODO history here
        db.execute(
            "INSERT INTO history (id, symbol, amount, time, price, state) VALUES(:id, :symbol, :amount, :time, :price, :state)",
            id=user_id, symbol=symbol, time=time, amount=shares, price=price, state="sell")
        if wallet == shares:
            # TODO delete wallet
            db.execute("DELETE FROM wallet WHERE id = :user_id AND symbol = :symbol AND amount = :shares",
                       user_id=user_id, symbol=symbol, shares=shares)
        else:
            db.execute("UPDATE wallet SET amount = amount-:shares WHERE id = :user_id AND symbol = :symbol",
                       user_id=user_id, symbol=symbol, shares=shares)

        cost = (price * shares) + cash
        # update cash
        db.execute("UPDATE users SET cash = :cost WHERE id = :user_id", user_id=user_id, cost=cost)

        return redirect("/")

    else:
        return render_template("sell.html", my_shares=my_shares)






def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
