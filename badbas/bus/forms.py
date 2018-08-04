# -*- coding: utf-8 -*-
"""Bus forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, HiddenField, SelectField, RadioField
from wtforms.validators import DataRequired, Optional, Length

from .models import Bus, Accusation, Report

import logging
logger = logging.getLogger(__name__)


class BusForm(FlaskForm):
    """
    A Bus Form
    """

    plate = StringField('Plate Number', validators=[DataRequired(), Length(min=4, max=10)])
    color = StringField('Color', validators=[DataRequired()])
    signage_front = StringField('Front Side Text', validators=[Optional(), Length(max=32)])
    signage_back = StringField('Back Side Text', validators=[Optional(), Length(max=32)])
    signage_left = StringField('Left Side Text', validators=[Optional(), Length(max=32)])
    signage_right = StringField('Right Side Text', validators=[Optional(), Length(max=32)])

    def __init__(self, *args, **kwargs):
        super(BusForm, self).__init__(*args, **kwargs)

    def validate(self):
        """Validate the form."""
        initial_validation = super(BusForm, self).validate()
        if not initial_validation:
            return False

        bus = Bus.query.filter_by(plate=self.plate.data).first()
        if bus:
            self.plate.errors.append('Bus already registered')
            return False

        return True


def NotFuture(form, field):
    logger.warn('Future Dates not Validated')
    pass


class ReportForm(FlaskForm):
    """
    A Report Form.
    """
    accusation_id = SelectField('Accusation', choices=[])

    lat = FloatField('Latitude')
    lng = FloatField('Longitude')
    area = StringField('Area', validators=[DataRequired(), Length(min=3, max=32)])
    time = RadioField('When', choices=[])

    def validate(self):
        initial_validation = super(ReportForm, self).validate()
        if not initial_validation:
            return False

        return True
