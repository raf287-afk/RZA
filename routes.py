from flask import render_template, request, url_for, redirect, session, flash
from models import User, ZooBooking, HotelBooking
from app import db
from datetime import datetime


def register_routes(app, db):

    # ---------------- HOME ----------------
    @app.route('/')
    def root_redirect():
        return redirect(url_for("home"))

    @app.route('/home')
    def home():
        return render_template(
            "index.html",
            logged_in=("userID" in session)
        )

    # ---------------- REGISTER ----------------
    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            # Convert the date string (YYYY-MM-DD) into a Python date
            dob = datetime.strptime(request.form["dob"], "%Y-%m-%d").date()

            new_user = User(
                username=request.form["username"],
                password=request.form["password"],  # hash later!
                email=request.form["email"],
                dateOfBirth=dob
            )

            db.session.add(new_user)
            db.session.commit()

            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("login"))  # Changed from "login_page" to "login"

        return render_template(
            "register.html",
            logged_in=("userID" in session)
        )

    # ---------------- LOGIN ----------------
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            user = User.query.filter_by(username=username).first()

            if user and user.password == password:   # Password hashing recommended later
                session["userID"] = user.userID
                flash("Login successful!", "success")
                return redirect(url_for("home"))

            else:
                flash("Invalid username or password.", "error")

        return render_template("login.html",
                               logged_in=("userID" in session))

    # ---------------- ACCOUNT PAGE ----------------
    @app.route("/account")
    def account():
        if "userID" not in session:
            return redirect(url_for("login"))

        userID = session["userID"]
        user = User.query.filter_by(userID=userID).first()

        # Always return lists, even if empty
        zoo_bookings = ZooBooking.query.filter_by(userID=userID).all() or []
        hotel_bookings = HotelBooking.query.filter_by(userID=userID).all() or []

        # Calculate total for template if needed
        total_bookings = len(zoo_bookings) + len(hotel_bookings)

        return render_template("account.html",
                               user=user,
                               zoo_bookings=zoo_bookings,
                               hotel_bookings=hotel_bookings,
                               total_bookings=total_bookings,  # Optional
                               logged_in=True)

    # ---------------- LOGOUT ----------------
    @app.route("/logout")
    def logout():
        session.clear()
        flash("Logged out successfully.", "success")
        return redirect(url_for("home"))

    # ---------------- ZOO BOOKING ----------------
    @app.route("/zoo_booking", methods=["GET", "POST"])
    def zoo_booking():

        if "userID" not in session:
            flash("Please log in to book your visit.", "error")
            return redirect(url_for("login"))

        if request.method == "POST":
            new_booking = ZooBooking(
                userID=session["userID"],
                ticketType=request.form["ticketType"],
                numberOfAdults=int(request.form["numberOfAdults"]),
                numberOfChildren=int(request.form["numberOfChildren"]),
                fullName=request.form["fullName"],
                visitDate=request.form["visitDate"]
            )

            db.session.add(new_booking)
            db.session.commit()

            flash("Your Zoo Booking was successful!", "success")
            return redirect(url_for("account"))

        return render_template("zoo_booking.html",
                               logged_in=True)


    # ---------------- HOTEL BOOKING ----------------
    @app.route("/hotel_booking", methods=["GET", "POST"])
    def hotel_booking():
        if "userID" not in session:
            flash("Please log in to access hotel bookings.", "error")
            return redirect(url_for("login"))

        if request.method == "POST":
            try:
                # Use CAMELCASE attribute names (matching your model)
                new_hotel_booking = HotelBooking(
                    userID=session["userID"],  # camelCase: userID
                    roomType=request.form["roomType"]  # camelCase: roomType
                )

                db.session.add(new_hotel_booking)
                db.session.commit()

                flash("Hotel booking successful!", "success")
                return redirect(url_for("account"))

            except Exception as e:
                db.session.rollback()
                flash(f"Error processing booking: {str(e)}", "error")
                return redirect(url_for("hotel_booking"))

        return render_template("hotel_booking.html", logged_in=True)