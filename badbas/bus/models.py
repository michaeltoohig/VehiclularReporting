# -*- coding: utf-8 -*-
"""Vehicle models."""
import datetime as dt

from badbas.database import Column, Model, SurrogatePK, db, reference_col, relationship


class Vehicle(SurrogatePK, Model):
    """
    A vehicle of the app.
    """

    __tablename__ = 'vehicles'

    plate_number = Column(db.String(16))
    plate_category_id = reference_col('plate_categories')
    plate_category = relationship('PlateCategory', back_populates='vehicles')

    vehicle_type_id = reference_col('vehicle_types')
    vehicle_type = relationship('VehicleType', back_populates='vehicles')

    primary_color_id = reference_col('VehicleColor')
    primary_color = relationship('vehicle_colors', foreign_keys=[primary_color_id])
    secondary_color_id = reference_col('VehicleColor')
    secondary_color = relationship('vehicle_colors', foreign_keys=[secondary_color_id])

    signage_front = Column(db.String(32))
    signage_back = Column(db.String(32))
    signage_left = Column(db.String(32))
    signage_right = Column(db.String(32))



    reports = relationship('Report', back_populates='vehicle')

    def __init__(self, *args, **kwargs):
        db.Model.__init__(self, *args, **kwargs)

    def __repr__(self):
        return '<Vehicle({0})>'.format(self.id)


class VehicleType(SurrogatePK, Model):
    """
    A type of vehicle license plates
    """

    __tablename__ = 'vehicle_types'
    name = Column(db.String(16))

    vehicles = relationship('vehicles', back_populates='type', lazy='dynamic')

    def __init__(self, *args, **kwargs):
        db.Model.__init__(self, *args, **kwargs)

    def __repr__(self):
        return '<VehicleType({0})>'.format(self.name)



class PlateCategory(SurrogatePK, Model):
    """
    A category of vehicle license plates
    """

    __tablename__ = 'plate_categories'
    name = Column(db.String(4))
    description = Column(db.String(32))

    vehicles = relationship('vehicles', back_populates='plate_category', lazy='dynamic')

    def __init__(self, *args, **kwargs):
        db.Model.__init__(self, *args, **kwargs)

    def __repr__(self):
        return '<PlateCategory({0})>'.format(self.name)


class VehicleColor(SurrogatePK, Model):
    """
    A color of vehicle
    """

    __tablename__ = 'vehicle_colors'
    name = Column(db.String(16))

    vehicles = relationship('vehicles', back_populates='color', lazy='dynamic')

    def __init__(self, *args, **kwargs):
        db.Model.__init__(self, *args, **kwargs)

    def __repr__(self):
        return '<VehicleColor({0})>'.format(self.name)



class Accusation(SurrogatePK, Model):
    """
    An accusation category against vehicles.
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
    A reported accusation against a vehicle.
    """

    __tablename__ = 'reports'
    user_id = reference_col('users')
    user = relationship('User')

    vehicle_id = reference_col('vehicles')
    vehicle = relationship('Vehicle', back_populates='reports')

    accusation_id = reference_col('accusations')
    accusation = relationship('Accusation')

    lat = Column(db.Float())
    lng = Column(db.Float())
    area = Column(db.String(32))

    time = Column(db.DateTime(), default=dt.datetime.utcnow())

    def __init__(self, *args, **kwargs):
        db.Model.__init__(self, *args, **kwargs)

    def __repr__(self):
        return '<Report(vehicle:{0}, user:{1}, accusation:{2})>'.format(self.vehicle_id, self.user_id, self.accusation_id)
