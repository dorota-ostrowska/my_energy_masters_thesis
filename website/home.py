from datetime import datetime, timedelta

from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from website.models import Invoice, Meter, Offer, Reading
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import io
import base64
import matplotlib.dates as mdates
from sqlalchemy import func

home = Blueprint("home", __name__)
matplotlib.use('Agg')


@home.route("/")
@home.route("/home")
def display_home():
    if current_user.is_authenticated:
        id_meter = Meter.query.filter_by(id_client=current_user.id_client).first().id_meter
        df = get_readings(id_meter, datetime.now().date(), datetime.now().date())
        chart = create_chart(df, datetime.now().date(), datetime.now().date())
        id_offer = Meter.query.filter_by(id_meter=id_meter).first().id_offer
        offer_name = Offer.query.filter_by(id_offer=id_offer).first().name
        number_of_unpaid_invoices = 0
        for invoice in get_invoices(current_user.id_client):
            if invoice.query.filter_by(is_it_paid=False):
                number_of_unpaid_invoices += 1
        return render_template("dashboard.html", username=current_user.name, current_offer=offer_name, num_unpaid_invoices=number_of_unpaid_invoices, chart_data=chart)
    return render_template("home.html")


@home.route("/")
@home.route("/home")
@login_required
def client_logged_in():
    return render_template("dashboard.html", user=current_user)


@home.route('/chart')
@login_required
def display_chart_of_energy_usage():
    id_meter = Meter.query.filter_by(id_client=current_user.id_client).first().id_meter
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    else:
        start_date = datetime.now().date()
        end_date = start_date
    if end_date < start_date:
        start_date, end_date = end_date, start_date
    df = get_readings(id_meter, start_date, end_date)
    chart = create_chart(df, start_date, end_date)
    return render_template('usage_chart.html', chart_data=chart)

def get_readings(id_meter: int, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    readings = Reading.query.filter(
        Reading.id_meter == id_meter,
        Reading.time >= start_date,
        Reading.time < end_date + timedelta(days=1)
    ).all()
    data = {
        "time": [reading.time for reading in readings],
        "used_energy": [reading.used_energy for reading in readings]
    }
    df = pd.DataFrame(data)
    return df

def create_chart(df: pd.DataFrame, start_date: datetime, end_date: datetime) -> bytes:
    _, ax = plt.subplots()
    if (end_date - start_date).days == 0:  # only one day - line chart
        df.plot(x='time', y='used_energy', ax=ax, kind='line', color='#018079')  # Zmiana koloru na #018079
        ax.set_title(f'Daily energy consumption on {start_date}')
        ax.set_xlabel('time')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H'))
        ax.set_ylabel('usage (kWh)')
    else:  # more days - bar chart
        df['date'] = pd.to_datetime(df['time']).dt.date
        df_grouped = df.groupby('date').agg({'used_energy': 'sum'}).reset_index()
        df_grouped.plot(x='date', y='used_energy', ax=ax, kind='bar', color='#018079')  # Zmiana koloru na #018079
        ax.set_title(f'Energy consumption in the period {start_date} - {end_date}')
        ax.set_xlabel('date')
        ax.set_ylabel('usage (kWh)')
    png_image = io.BytesIO()
    plt.savefig(png_image, format='png')
    png_image.seek(0)
    png_base64 = base64.b64encode(png_image.getvalue()).decode('ascii')
    return png_base64

@home.route('/invoice')
@login_required
def display_invoices():
    invoices = get_invoices(current_user.id_client)
    return render_template('invoice.html', invoices=invoices)

def get_invoices(id_client: int):
    id_meter = Meter.query.filter_by(id_client=id_client).first().id_meter
    invoices = Invoice.query.filter(Invoice.id_meter==id_meter, Invoice.used_energy>0).all()
    for invoice in invoices:
        invoice.amount_to_pay = round(invoice.amount_to_pay, 2)
        invoice.billing_period = invoice.billing_period.strftime('%B %Y')
        invoice.date_of_issue = invoice.date_of_issue.strftime('%Y-%m-%d %H:%M')
    return invoices
