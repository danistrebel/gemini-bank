from app import app, db, login
from flask import request, render_template, redirect, url_for, flash
from models import User, Account, Transaction, RecurringPayment
from forms import RegisterForm, LoginForm, CreateAccountForm, TransactionForm, RecurringPaymentForm
from flask_login import login_required, login_user, logout_user, current_user
from utils import convert_to_eur, get_next_date
from datetime import datetime


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@login.unauthorized_handler
def unauthorized():
    return redirect(url_for("login"))

@app.route("/")
def index():
    if current_user.is_authenticated:
        user = current_user
    else:
        user = "anonymous"
    return render_template("index.html", user = user)


@app.route("/register", methods = ["GET","POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(firstname = form.firstname.data, lastname = form.lastname.data, email = form.email.data)
        user.set_password(form.password1.data)
        db.session.add(user)
        try:
            db.session.commit()
            flash(f"User {user} registered correctly")
        except:
            db.session.rollback()
            flash("Problems in registration")
        return redirect(url_for('index'))           
    return render_template("register.html", form = form)


@app.route("/login", methods = ["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("mybank"))
        else:
            return redirect(url_for('login'))
    return render_template("login.html", form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/mybank", methods = ["GET","POST"])
@login_required
def mybank():
    if current_user.is_authenticated:
        user = current_user
    else:
        user = "anonymous"
    accounts = User.query.get(current_user.id).accounts.all()
    form = CreateAccountForm()
    if form.validate_on_submit():
        account = Account(balance=0,number=(160000+(Account.query.count())+1),user_id=current_user.id)
        db.session.add(account)
        try:
            db.session.commit()
            flash(f"Account {account.number} created successfully")
        except:
            db.session.rollback()
            flash(f"Problem in account creation")
        return redirect(url_for('account', id=account.id))
    return render_template("mybank.html", user = user, accounts = accounts, form = form)

@app.route("/accounts/<int:id>", methods = ["GET","POST"])
@login_required
def account(id):
    if current_user.is_authenticated:
        user = current_user
    else:
        user = "anonymous"
    account = Account.query.get(id)
    transactions = Transaction.query.filter_by(account_id=id).all()
    return render_template("account.html", user = user, account = account, transactions = transactions)

@app.route("/<int:id>/transaction", methods = ["GET","POST"])
@login_required
def transaction(id):
    if current_user.is_authenticated:
        user = current_user
    else:
        user = "anonymous"
    form = TransactionForm()
    account = Account.query.get(id)
    if form.validate_on_submit():
        amount_eur = convert_to_eur(form.amount.data, form.currency.data)
        if form.type.data == "deposit":
            transaction = Transaction(amount = amount_eur, type = form.type.data, description = form.description.data, account_id=id)
        else:
            transaction = Transaction(amount = -(amount_eur), type = form.type.data, description = form.description.data, account_id=id)
        db.session.add(transaction)
        account.balance += transaction.amount
        try:
            flash(f"{form.type.data } completed correctly")
            db.session.commit()
            return redirect(url_for('account', id=id))
        except:
            flash(f"{form.type.data } failed")
            db.session.rollback()           
            return redirect(url_for('transaction', id=id))
    return render_template("transaction.html", user = user, account = account, form = form, user_accounts_count = user.accounts.count())

@app.route("/accounts/<int:id>/recurring")
@login_required
def recurring_payments(id):
    if current_user.is_authenticated:
        user = current_user
    else:
        user = "anonymous"
    account = Account.query.get(id)
    # Security check: ensure user owns account
    if account.user_id != current_user.id:
         flash("You do not have permission to view this account.")
         return redirect(url_for('mybank'))
         
    payments = RecurringPayment.query.filter_by(account_id=id).all()
    return render_template("recurring_payments.html", user = user, account = account, payments = payments)

@app.route("/accounts/<int:id>/recurring/new", methods = ["GET","POST"])
@login_required
def create_recurring_payment(id):
    if current_user.is_authenticated:
        user = current_user
    else:
        user = "anonymous"
    form = RecurringPaymentForm()
    account = Account.query.get(id)
    if account.user_id != current_user.id:
         flash("You do not have permission to view this account.")
         return redirect(url_for('mybank'))

    if form.validate_on_submit():
        amount_eur = convert_to_eur(form.amount.data, form.currency.data)
        payment = RecurringPayment(
            amount = amount_eur,
            description = form.description.data,
            account_id = id,
            frequency = form.frequency.data,
            start_date = datetime.combine(form.start_date.data, datetime.min.time()),
            end_date = datetime.combine(form.end_date.data, datetime.min.time()) if form.end_date.data else None,
            next_payment_date = datetime.combine(form.start_date.data, datetime.min.time())
        )
        db.session.add(payment)
        try:
            db.session.commit()
            flash("Recurring payment set up successfully")
            return redirect(url_for('recurring_payments', id=id))
        except:
            db.session.rollback()
            flash("Failed to set up recurring payment")
    
    return render_template("create_recurring_payment.html", user = user, account = account, form = form)

@app.route("/recurring/<int:id>/delete")
@login_required
def delete_recurring_payment(id):
    payment = RecurringPayment.query.get(id)
    if payment:
        account = Account.query.get(payment.account_id)
        if account.user_id == current_user.id:
            db.session.delete(payment)
            db.session.commit()
            flash("Recurring payment cancelled")
            return redirect(url_for('recurring_payments', id=account.id))
    
    flash("Action not allowed")
    return redirect(url_for('mybank'))

@app.route("/process_recurring")
def process_recurring():
    now = datetime.now()
    payments = RecurringPayment.query.filter(RecurringPayment.next_payment_date <= now).all()
    count = 0
    for payment in payments:
        if payment.end_date and now > payment.end_date:
            continue
            
        # Create transaction
        transaction = Transaction(
            amount = -(payment.amount), 
            type = "recurring", 
            description = f"Recurring: {payment.description}", 
            account_id = payment.account_id,
            date = now
        )
        db.session.add(transaction)
        
        # Update balance
        account = Account.query.get(payment.account_id)
        account.balance += transaction.amount # amount is negative
        
        # Update next date
        payment.next_payment_date = get_next_date(payment.next_payment_date, payment.frequency)
        count += 1
        
    db.session.commit()
    return f"Processed {count} recurring payments."