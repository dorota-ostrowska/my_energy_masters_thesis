"""
This module defines the database models for a web application using SQLAlchemy and Flask-Login.

The module contains the following classes:

1. Post: Represents a post in the forum.
2. Comment: Represents a comment on a post.
3. Favourite: Represents a like on a post.
4. Client: Represents a client.
5. Address: Represents an address.
6. Meter: Represents a meter.
7. Reading: Represents a reading from a meter.
8. Offer: Represents an offer.
9. Challenge: Represents a challenge.
10. CustomizedChallenge: Represents a customized challenge for a client.
11. Invoice: Represents an invoice.

Each class is defined as a SQLAlchemy model with various attributes and relationships to other models.
These models are used to create, read, update, and delete records in the corresponding database tables.
Flask-Login is used to manage user sessions and authentication.
"""

from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Post(db.Model):
    """
    Represents a post in the forum.

    Attributes:
        id_post (int): Primary key for the post.
        text (str): Content of the post.
        date_created (datetime): Timestamp of when the post was created.
        id_author (int): Foreign key referencing the client who authored the post.
        comments (relationship): Relationship to the Comment model.
        likes (relationship): Relationship to the Favourite model.
    """

    __tablename__ = "post"
    id_post = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    id_author = db.Column(
        db.Integer,
        db.ForeignKey("client.id_client", ondelete="CASCADE"),
        nullable=False,
    )
    comments = db.relationship(
        "Comment", backref="comments_under_post", cascade="all, delete-orphan"
    )
    likes = db.relationship(
        "Favourite", backref="likes_under_post", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f'<Client "{self.author}">'

    def get_id(self):
        return self.id_post


class Comment(db.Model):
    """
    Represents a comment on a post.

    Attributes:
        id_comment (int): Primary key for the comment.
        text (str): Content of the comment.
        date_created (datetime): Timestamp of when the comment was created.
        id_author (int): Foreign key referencing the client who authored the comment.
        id_post (int): Foreign key referencing the post this comment belongs to.
    """

    __tablename__ = "comment"
    id_comment = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    id_author = db.Column(
        db.Integer,
        db.ForeignKey("client.id_client", ondelete="CASCADE"),
        nullable=False,
    )
    id_post = db.Column(db.Integer, db.ForeignKey("post.id_post", ondelete="CASCADE"))

    def __repr__(self):
        return f'<Client "{self.author}">'

    def get_id(self):
        return self.id_comment


class Favourite(db.Model):
    """
    Represents a like on a post.

    Attributes:
        id_like (int): Primary key for the like.
        date_created (datetime): Timestamp of when the like was created.
        id_author (int): Foreign key referencing the client who liked the post.
        id_post (int): Foreign key referencing the post that was liked.
    """

    __tablename__ = "favourite"
    id_like = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    id_author = db.Column(
        db.Integer,
        db.ForeignKey("client.id_client", ondelete="CASCADE"),
        nullable=False,
    )
    id_post = db.Column(
        db.Integer, db.ForeignKey("post.id_post", ondelete="CASCADE"), nullable=False
    )

    def __repr__(self):
        return f'<Client "{self.author}">'

    def get_id(self):
        return self.id_like


class Client(db.Model, UserMixin):
    """
    Represents a client.

    Attributes:
        id_client (int): Primary key for the client.
        username (str): Username of the client.
        name (str): First name of the client.
        surname (str): Last name of the client.
        pesel (str): Unique PESEL number of the client.
        points (int): Points accumulated by the client.
        id_clients_mailing_address (int): Foreign key referencing the client's mailing address.
        email (str): Email address of the client.
        password (str): Password of the client.
        member_of_challenge (bool): Indicates if the client is a member of a challenge.
        number_of_rooms (int): Number of rooms in the client's residence.
        number_of_residents (int): Number of residents in the client's residence.
        meter (relationship): Relationship to the Meter model.
        posts (relationship): Relationship to the Post model.
        comments (relationship): Relationship to the Comment model.
        likes (relationship): Relationship to the Favourite model.
        customizedchallenges (relationship): Relationship to the CustomizedChallenge model.
    """

    __tablename__ = "client"
    id_client = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=True)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    pesel = db.Column(db.String(11), unique=True)
    points = db.Column(db.Integer)
    id_clients_mailing_address = db.Column(
        db.Integer, db.ForeignKey("address.id_address")
    )
    email = db.Column(db.String(50), unique=True, nullable=True)
    password = db.Column(db.Text, nullable=True)
    member_of_challenge = db.Column(db.Boolean, nullable=True)
    number_of_rooms = db.Column(db.Integer, nullable=True)
    number_of_residents = db.Column(db.Integer, nullable=True)
    meter = db.relationship(
        "Meter", backref="clients_meter", cascade="all, delete-orphan"
    )
    posts = db.relationship(
        "Post",
        backref="users_posts",
        passive_deletes=True,
        cascade="all, delete-orphan",
    )
    comments = db.relationship(
        "Comment", backref="users_comments", cascade="all, delete-orphan"
    )
    likes = db.relationship(
        "Favourite", backref="users_likes", cascade="all, delete-orphan"
    )
    customizedchallenges = db.relationship(
        "CustomizedChallenge",
        backref="challenge_for_client",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f'<Client "{self.name} {self.surname}">'

    def get_id(self):
        return self.id_client


class Address(db.Model, UserMixin):
    """
    Represents an address.

    Attributes:
        id_address (int): Primary key for the address.
        street (str): Street name of the address.
        house_number (str): House number of the address.
        local_number (str): Local number of the address.
        zip_code (str): Zip code of the address.
        city (str): City of the address.
        additional_info (str): Additional information for the address.
        clients (relationship): Relationship to the Client model.
    """

    __tablename__ = "address"
    id_address = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(50))
    house_number = db.Column(db.String(5))
    local_number = db.Column(db.String(5))
    zip_code = db.Column(db.String(6))
    city = db.Column(db.String(50))
    additional_info = db.Column(db.String(50), nullable=True)
    clients = db.relationship("Client", backref="address")

    def __repr__(self):
        return f'<Address "{self.street}">'

    def get_id(self):
        return self.id_address


class Meter(db.Model, UserMixin):
    """
    Represents a meter.

    Attributes:
        id_meter (int): Primary key for the meter.
        id_client (int): Foreign key referencing the client who owns the meter.
        ppe (str): PPE number of the meter.
        id_offer (int): Foreign key referencing the offer associated with the meter.
        readings (relationship): Relationship to the Reading model.
        invoices (relationship): Relationship to the Invoice model.
    """

    __tablename__ = "meter"
    id_meter = db.Column(db.Integer, primary_key=True)
    id_client = db.Column(db.Integer, db.ForeignKey("client.id_client"))
    ppe = db.Column(db.String(18))
    id_offer = db.Column(db.Integer, db.ForeignKey("offer.id_offer"))
    readings = db.relationship("Reading", backref="reading")
    invoices = db.relationship("Invoice", backref="invoices")

    def __repr__(self):
        return f'<Meter "{self.id_meter}">'

    def get_id(self):
        return self.id_meter


class Reading(db.Model, UserMixin):
    """
    Represents a reading from a meter.

    Attributes:
        id_reading (int): Primary key for the reading.
        time (datetime): Timestamp of when the reading was taken.
        used_energy (float): Amount of energy used.
        id_meter (int): Foreign key referencing the meter the reading belongs to.
    """

    __tablename__ = "reading"
    id_reading = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    used_energy = db.Column(db.Float)
    id_meter = db.Column(db.Integer, db.ForeignKey("meter.id_meter"))

    def __repr__(self):
        return f'<Meter "{self.id_reading}">'

    def get_id(self):
        return self.id_reading


class Offer(db.Model, UserMixin):
    """
    Represents an offer.

    Attributes:
        id_offer (int): Primary key for the offer.
        name (str): Name of the offer.
        tarrif (str): Tariff of the offer.
        pv_installation (bool): Indicates if the offer includes PV installation.
        meters (relationship): Relationship to the Meter model.
    """

    __tablename__ = "offer"
    id_offer = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    tarrif = db.Column(db.String(50))
    pv_installation = db.Column(db.Boolean)
    kwh_price = db.Column(db.Float)
    meters = db.relationship("Meter", backref="meters_in_offer")

    def __repr__(self):
        return f'<Meter "{self.id_offer}">'

    def get_id(self):
        return self.id_offer


class Challenge(db.Model, UserMixin):
    """
    Represents a challenge.

    Attributes:
        id_challenge (int): Primary key for the challenge.
        name (str): Name of the challenge.
        type_small_big (bool): Indicates the type of the challenge (small or big).
        description (str): Description of the challenge.
        customizing_function (str): Customizing function for the challenge.
        customizedchallenges (relationship): Relationship to the CustomizedChallenge model.
    """

    __tablename__ = "challenge"
    id_challenge = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    type_small_big = db.Column(db.Boolean)
    description = db.Column(db.Text)
    customizing_function = db.Column(db.String(50))
    customizedchallenges = db.relationship(
        "CustomizedChallenge", backref="customized_challenge"
    )

    def __repr__(self):
        return f'<Challenge "{self.name}">'

    def get_id(self):
        return self.id_challenge


class CustomizedChallenge(db.Model, UserMixin):
    """
    Represents a customized challenge for a client.

    Attributes:
        id_customized_challenge (int): Primary key for the customized challenge.
        id_client (int): Foreign key referencing the client.
        id_challenge (int): Foreign key referencing the challenge.
        is_done (bool): Indicates if the challenge is completed.
        points_scored (int): Points scored by the client for the challenge.
        start_date (date): Start date of the challenge.
        end_date (date): End date of the challenge.
    """

    __tablename__ = "customizedchallenge"
    id_customized_challenge = db.Column(db.Integer, primary_key=True)
    id_client = db.Column(db.Integer, db.ForeignKey("client.id_client"))
    id_challenge = db.Column(db.Integer, db.ForeignKey("challenge.id_challenge"))
    is_done = db.Column(db.Boolean, nullable=True)
    points_scored = db.Column(db.Integer)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f'<CustomizedChallenge "{self.task_description}">'

    def get_id(self):
        return self.id_meter, self.id_challenge


class Invoice(db.Model, UserMixin):
    """
    Represents an invoice.

    Attributes:
        id_invoice (int): Primary key for the invoice.
        id_meter (int): Foreign key referencing the meter.
        date_of_issue (date): Date of issue of the invoice.
        amount_to_pay (float): Amount to be paid.
        used_energy (float): Amount of energy used.
        billing_period (datetime): Billing period of the invoice.
        is_it_paid (bool): Indicates if the invoice is paid.
    """

    __tablename__ = "invoice"
    id_invoice = db.Column(db.Integer, primary_key=True)
    id_meter = db.Column(db.Integer, db.ForeignKey("meter.id_meter"))
    date_of_issue = db.Column(db.Date)
    amount_to_pay = db.Column(db.Float)
    used_energy = db.Column(db.Float)
    billing_period = db.Column(db.DateTime)
    is_it_paid = db.Column(db.Boolean)
