# -*- coding: utf-8 -*-
"""Bus models."""
import datetime as dt

from badbas.database import Column, Model, SurrogatePK, db, reference_col, relationship


class Bus(SurrogatePK, Model):
    """
    A bus of the app.
    """

    __tablename__ = 'buses'
    plate = Column(db.String(16))
    government = Column(db.Boolean(), default=False)
    # bus name usually on the window in front
    color = Column(db.String(16))
    #model = Column(db.String(16))
    #box = Column(db.Boolean(), default=False)
    signage_front = Column(db.String(32))
    signage_back = Column(db.String(32))
    signage_left = Column(db.String(32))
    signage_right = Column(db.String(32))

    reports = relationship('Report', back_populates='bus')

    def __init__(self, *args, **kwargs):
        db.Model.__init__(self, *args, **kwargs)

    def __repr__(self):
        return '<Bus({0})>'.format(self.id)


class Accusation(SurrogatePK, Model):
    """
    An accusation category against buses.
    Examples include: accident, smoke, speed, etc
    """

    __tablename__ = 'accusations'
    name = Column(db.String(16))

    def __init__(self, *args, **kwargs):
        db.Model.__init__(self, *args, **kwargs)

    def __repr__(self):
        return '<Accusation({0})>'.format(self.name)


class Report(SurrogatePK, Model):
    """
    A reported accusation against a bus.
    """

    __tablename__ = 'reports'
    user_id = reference_col('users')
    user = relationship('User')

    bus_id = reference_col('buses')
    bus = relationship('Bus', back_populates='reports')

    accusation_id = reference_col('accusations')
    accusation = relationship('Accusation')

    lat = Column(db.Float())
    lng = Column(db.Float())
    area = Column(db.String(32))

    time = Column(db.DateTime(), default=dt.datetime.utcnow())

    def __init__(self, *args, **kwargs):
        db.Model.__init__(self, *args, **kwargs)

    def __repr__(self):
        return '<Report(bus:{0}, user:{1}, accusation:{2})>'.format(self.bus_id, self.user_id, self.accusation_id)
