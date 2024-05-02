from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Post(db.Model):
    __tablename__ = "post"
    id_post = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    id_author = db.Column(
        db.Integer,
        db.ForeignKey("client.id_client", ondelete="CASCADE"),
        nullable=False,
    )
    comments = db.relationship("Comment", backref="comments_under_post", cascade="all, delete-orphan")
    likes = db.relationship("Favourite", backref="likes_under_post", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Client "{self.author}">'

    def get_id(self):
        return self.id_post


class Comment(db.Model):
    __tablename__ = "comment"
    id_comment = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    id_author = db.Column(
        db.Integer,
        db.ForeignKey("client.id_client", ondelete="CASCADE"),
        nullable=False,
    )
    id_post = db.Column(
        db.Integer, db.ForeignKey("post.id_post", ondelete="CASCADE")
    )

    def __repr__(self):
        return f'<Client "{self.author}">'

    def get_id(self):
        return self.id_comment


class Favourite(db.Model):
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
    __tablename__ = "client"
    id_client = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    pesel = db.Column(db.String(11), unique=True)
    id_clients_mailing_address = db.Column(
        db.Integer, db.ForeignKey("address.id_address")
    )
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.Text)
    meters = db.relationship("Meter", backref="meter_for_client", cascade="all, delete-orphan")
    posts = db.relationship("Post", backref="users_posts", passive_deletes=True, cascade="all, delete-orphan")
    comments = db.relationship("Comment", backref="users_comments", cascade="all, delete-orphan")
    likes = db.relationship("Favourite", backref="users_likes", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Client "{self.name} {self.surname}">'

    def get_id(self):
        return self.id_client


class Address(db.Model, UserMixin):
    __tablename__ = "address"
    id_address = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(50))
    house_number = db.Column(db.String(5))
    local_number = db.Column(db.String(5))
    zip_code = db.Column(db.String(6))
    city = db.Column(db.String(50))
    additional_info = db.Column(db.String(50), nullable=True)
    clients = db.relationship("Client", backref="address")
    meters = db.relationship("Meter", backref="address_of_meter")

    def __repr__(self):
        return f'<Address "{self.street}">'

    def get_id(self):
        return self.id_address


class Meter(db.Model, UserMixin):
    __tablename__ = "meter"
    id_meter = db.Column(db.Integer, primary_key=True)
    id_owner = db.Column(db.Integer, db.ForeignKey("client.id_client"))
    id_meters_place_address = db.Column(db.Integer, db.ForeignKey("address.id_address"))
    member_of_challange = db.Column(db.Boolean)
    ranking_points = db.Column(db.Integer)
    number_of_rooms = db.Column(db.Integer, nullable=True)
    number_of_residents = db.Column(db.Integer, nullable=True)
    readings = db.relationship("Reading", backref="reading")
    offersformeters = db.relationship("OfferForMeter", backref="offerformeter_meter", cascade="all, delete-orphan")
    customizedchallanges = db.relationship("CustomizedChallange", backref="challange_for_meter", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Meter "{self.id_meter}">'

    def get_id(self):
        return self.id_meter


class Reading(db.Model, UserMixin):
    __tablename__ = "reading"
    id_reading = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    used_energy = db.Column(db.Float)
    meters = db.Column(db.Integer, db.ForeignKey("meter.id_meter"))

    def __repr__(self):
        return f'<Meter "{self.id_reading}">'

    def get_id(self):
        return self.id_reading


class Offer(db.Model, UserMixin):
    __tablename__ = "offer"
    id_offer = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    tarrif = db.Column(db.String(50))
    pv_installation = db.Column(db.Boolean)
    offersformeters = db.relationship("OfferForMeter", backref="offerformeter_offer")

    def __repr__(self):
        return f'<Meter "{self.id_offer}">'

    def get_id(self):
        return self.id_offer


class OfferForMeter(db.Model, UserMixin):
    __tablename__ = "offerformeter"
    id_offer_for_meter = db.Column(db.Integer, primary_key=True)
    id_offers_type = db.Column(db.Integer, db.ForeignKey("offer.id_offer"))
    id_meter = db.Column(db.Integer, db.ForeignKey("meter.id_meter"))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f'<Meter "{self.id_offerformeter}">'

    def get_id(self):
        return self.id_offerformeter


class Challange(db.Model, UserMixin):
    __tablename__ = "challange"
    id_challange = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    type_small_big = db.Column(db.Boolean) 
    description = db.Column(db.Text)
    customizedchallanges = db.relationship("CustomizedChallange", backref="customized_challange")

    def __repr__(self):
        return f'<Challange "{self.name}">'

    def get_id(self):
        return self.id_challange
    

class CustomizedChallange(db.Model, UserMixin):
    __tablename__ = "customizedchallange"
    id_customized_challange = db.Column(db.Integer, primary_key=True)
    id_meter = db.Column(db.Integer, db.ForeignKey("meter.id_meter"))
    id_challange = db.Column(db.Integer, db.ForeignKey("challange.id_challange"))
    is_done = db.Column(db.Boolean, nullable = True)
    points_scored = db.Column(db.Integer)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f'<CustomizedChallange "{self.task_description}">'

    def get_id(self):
        return self.id_meter, self.id_challange
    