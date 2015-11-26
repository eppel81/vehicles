from my_app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


# table for many-to-many (Users <-> vehicles relations)
# object2user = db.Table(
#     'object2user',
#     db.Column('user_id', db.Integer, db.ForeignKey('users.nid')),
#     db.Column('object_id', db.Integer, db.ForeignKey('objects.nid')),
#     db.Column('visible', db.Boolean, default=True))


class Object2user(db.Model):
    """
    Associated object for many-to-many link
    """
    __tablename__ = 'object2user'
    # id = db.Column(db.Integer, primary_key=True)

    # for db.table
    user_id = db.Column(db.Integer, db.ForeignKey('users.nid'), primary_key=True)
    object_id = db.Column(db.Integer, db.ForeignKey('objects.nid'), primary_key=True)
    visible = db.Column(db.Boolean)
    object = db.relationship('Objects', backref='users')

    def __init__(self):
        self.visible = True


class Users(db.Model):
    """
    All registered users
    """
    nid = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100))
    locked = db.Column(db.Boolean)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    admin = db.Column(db.Integer, default=0)
    lastlogin = db.Column(db.DateTime(timezone=True))
    lastfailedlogin = db.Column(db.DateTime(timezone=True))
    failcount = db.Column(db.Integer)

    # for db.table
    # vehicles = db.relationship('Objects', secondary=Object2user,
    #                            backref=db.backref('user', lazy='dynamic'))

    vehicles = db.relationship('Object2user', backref='user', lazy='dynamic',  cascade="all, delete, delete-orphan")

    def __init__(self, login, password, name):
        self.login = login
        self.password = generate_password_hash(password)
        self.name = name

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.nid)

    def __repr__(self):
        return 'User: %s/%s/%s' % (self.login, self.password, self.name)

    def change_pass(self, password):
        self.password = generate_password_hash(password)

    def add_vehicle(self, obj):
        """
        Add object to user
        """
        if not self.is_owned(obj):
            assoc = Object2user()
            assoc.object = obj
            self.vehicles.append(assoc)
            return self

    def del_vehicle(self, obj):
        """
        Delete object from user
        """
        if self.is_owned(obj):
            assoc = Object2user.query.filter_by(user_id=self.nid, object_id=obj.nid).first()
            self.vehicles.remove(assoc)
            return self

    def is_owned(self, obj):
        return self.vehicles.filter_by(object_id=obj.nid).count() > 0

    def hide_show_vehicle(self, obj):
        """
        Change attr at object (vehicle)
        """
        assoc = Object2user.query.filter_by(user_id=self.nid, object_id=obj.nid).first()
        if assoc.visible:
            assoc.visible = False
        else:
            assoc.visible = True
        return self

    def change_password(self, password):
        """
        Change user's password
        """
        self.password = generate_password_hash(password)


class Providers(db.Model):
    """
    Providers
    """
    nid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Provider : %s' % self.name


class Objects(db.Model):
    """
    Vehicles
    """
    nid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    valid_from = db.Column(db.DateTime, default=datetime.utcnow)
    valid_to = db.Column(db.DateTime)
    created_by = db.Column(db.Integer)
    provider_id = db.Column(db.Integer, db.ForeignKey('providers.nid'))
    created = db.Column(db.DateTime(timezone=True))
    nofqueries = db.Column(db.Integer)
    nofsqueries = db.Column(db.Integer)
    lastquery = db.Column(db.DateTime(timezone=True))
    active = db.Column(db.Boolean)
    # backref for locations. Attention at backref!!!
    locations = db.relationship('Location', backref='object', lazy='dynamic')

    def __init__(self, name, ):
        self.name = name

    def __repr__(self):
        return 'Vehicle : %s' % (self.name, )


class Location(db.Model):
    """
    Coords of vehicles at explicit time
    """
    nid = db.Column(db.Integer, primary_key=True)
    ts = db.Column(db.DateTime(timezone=True), nullable=False)
    object_id = db.Column(db.Integer, db.ForeignKey('objects.nid'))
    bssid = db.Column(db.String(50))
    longitude = db.Column(db.NUMERIC(precision=11, scale=6))
    latitude = db.Column(db.NUMERIC(precision=11, scale=6))
    azimuth = db.Column(db.NUMERIC(precision=10, scale=2))
    distance = db.Column(db.NUMERIC(precision=10, scale=2))
    other = db.Column(db.Text)

    def __init__(self, object_id, ts, longitude, latitude):
        self.object_id = object_id
        self.ts = ts
        self.longitude = longitude
        self.latitude = latitude

    def __repr__(self):
        return 'Object %s and it\'s coords [%s, %s] at time %s' % (self.object_id,
                                                                   str(self.latitude),
                                                                   str(self.longitude),
                                                                   str(self.ts))

class Settings(db.Model):
    """
    System settings
    """
    nid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    value = db.Column(db.String())
    description = db.Column(db.String())
    max_objects = db.Column(db.Integer, default=10)
    max_points = db.Column(db.Integer, default=200)


