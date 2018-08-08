# -*- coding: utf-8 -*-
"""Bus views."""
import datetime as dt

from flask import Blueprint, render_template, abort, flash, url_for, request, redirect
from flask_login import login_required, current_user
from sqlalchemy.orm.exc import NoResultFound

from badbas.extensions import limiter
from badbas.utils import flash_errors
from .models import Bus, Report, Accusation
from .forms import BusForm, ReportForm

blueprint = Blueprint('vehicle', __name__, url_prefix='/vehicle', static_folder='../static')


@blueprint.route('/list')
def list():
    """List buses."""
    vehicles = Bus.query.all()
    return render_template('vehicles/list.html', vehicles=vehicles)


@blueprint.route('/search')
def search():
    """Search vehicles."""
    pass


@blueprint.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    """Create a new bus."""
    form = BusForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            bus = Bus()
            bus.plate = form.plate.data
            bus.government = True if form.plate.data.lower().startswith('g') else False
            bus.color = form.color.data
            bus.signage_front = form.signage_front.data
            bus.signage_back = form.signage_back.data
            bus.signage_left = form.signage_left.data
            bus.signage_right = form.signage_right.data
            bus.save()
            flash('Vehicle added', 'success')
            return redirect(url_for('.list'))
        else:
            flash_errors(form)
    return render_template('vehicles/form.html', form=form)


@blueprint.route('/<int:id>')
def vehicle(id):
    try:
        vehicle = Bus.query.filter_by(id=id).one()
    except NoResultFound:
        return abort(404)

    return render_template('vehicles/vehicle.html', vehicle=vehicle)


@blueprint.route('/reports')
@login_required
def reports():
    """List Reports."""
    pass


def report_limiting(bus_id, user_id):
    today = dt.datetime.utcnow().today()
    start = dt.datetime(year=today.year, month=today.month, day=today.day)
    tomorrow = today + dt.timedelta(days=1)
    end = dt.datetime(year=tomorrow.year, month=tomorrow.month, day=tomorrow.day)
    # Make the filter searching for a report within the current calendar day
    _query_user = Report.query.filter_by(user_id=user_id)
    _query_bus = _query_user.filter_by(bus_id=bus_id)
    report = _query_bus.filter(Report.time >= start).filter(Report.time <= end).first()
    if report:
        return True
    reports = _query_user.filter(Report.time >= start).filter(Report.time <= end).all()
    if len(reports) >= 5:
        return True
    return False


def make_time_choices():
    """
    Return a list of choices when the report incident occured.
    Depending on time of day the choices will vary.
    """
    static_choices = [
        (0, 'Just Now'),
        (1, '15 Minutes Ago'),
        (2, 'An Hour Ago'),
        (3, 'Earlier Today'),
        (4, 'Yesterday')
    ]
    now = dt.datetime.utcnow()
    selection_times = [
        now,
        now - dt.timedelta(minutes=15),
        now - dt.timedelta(hours=1),
        now - dt.timedelta(hours=6),
        now - dt.timedelta(days=1)
    ]
    return static_choices, selection_times


def AccusationList():
    accusations = Accusation.query.all()
    return [(a.id, a.name) for a in accusations]


@blueprint.route('<int:bus_id>/reports/new', methods=['GET', 'POST'])
@login_required
def reports_new(bus_id):
    if report_limiting(bus_id, current_user.id):
        flash('You reached the limit of reports you can make today', 'warning')
        return redirect(url_for('.list'))
    form = ReportForm()
    form.time.choices, selection_datetimes = make_time_choices()
    form.accusation_id.choices = AccusationList()
    if request.method == 'POST':
        if form.validate_on_submit():
            report = Report()
            report.user_id = current_user.id
            report.bus_id = bus_id
            report.accusation_id = form.accusation_id.data
            report.area = form.area.data
            report.time = selection_datetimes[1]
            report.save()
            flash('Report added', 'success')
            return redirect(url_for('.bus', id=bus_id))
        else:
            flash_errors(form)
    return render_template('vehicles/form_report.html', form=form)
