from flask_sqlalchemy import SQLAlchemy
from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "user"

    userID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    dateOfBirth = db.Column(db.Date, nullable=False)

    def __init__(self, username, password, email, dateOfBirth):
        self.username = username
        self.password = password
        self.email = email
        self.dateOfBirth = dateOfBirth


class HotelBooking(db.Model):
    __tablename__ = 'hotel_booking'  # WITH underscore!

    hotelBookingID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userID = db.Column(db.Integer, nullable=False)
    roomType = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<HotelBooking {self.hotelBookingID} - {self.roomType}>'


class ZooBooking(db.Model):
    __tablename__ = "zoo_booking"

    zooBookingID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userID = db.Column(db.Integer, db.ForeignKey("user.userID"), nullable=False)
    ticketType = db.Column(db.String(45), nullable=False)

    numberOfAdults = db.Column(db.Integer, nullable=False)
    numberOfChildren = db.Column(db.Integer, nullable=False)
    fullName = db.Column(db.String(100), nullable=False)
    visitDate = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<ZooBooking {self.zooBookingID}>"

    def __init__(self, userID, ticketType, numberOfAdults, numberOfChildren, fullName, visitDate):
        self.userID = userID
        self.ticketType = ticketType
        self.numberOfAdults = numberOfAdults
        self.numberOfChildren = numberOfChildren
        self.fullName = fullName
        self.visitDate = visitDate

class Ticket(db.Model):
    __tablename__ = "ticket"
    ticket_id = db.Column(db.Integer, primary_key=True, nullable=False)
    ticketbooking_id = db.Column(db.Integer, db.ForeignKey("ticket_booking.ticketbooking_id"), nullable=False)

    def __init__(self, ticketbooking_id):
        self.ticketbooking_id = ticketbooking_id




