import pandas as pd
import plotly.express as px
from database import DatabaseManager


db = DatabaseManager()


def phishing_trend():
    df = pd.DataFrame(db.fetch_all('cyber_incidents'),
    columns=['id','category','severity','status','resolution_time','date'])
    df = df.drop(columns=["date"])
    return px.bar(df, x='category', y='resolution_time', title='Incident Resolution Time')


def dataset_usage():
    df = pd.DataFrame(db.fetch_all('datasets'),
    columns=['id','name','size','rows','source','date'])
    df = df.drop(columns=["date"])
    return px.scatter(df, x='rows', y='size', title='Dataset Resource Usage')


def ticket_delay():
    df = pd.DataFrame(db.fetch_all('it_tickets'),
    columns=['id','staff','status','time','date'])
    df = df.drop(columns=["date"])
    return px.bar(df, x='staff', y='time', title='IT Ticket Delays')

def cyber_time_series():
    df = pd.read_sql("SELECT * FROM cyber_incidents", db.conn)
    df["reported_date"] = pd.to_datetime(df["reported_date"])

    trend = (
        df.groupby([df["reported_date"].dt.date, "category"])
        .size()
        .reset_index(name="count")
    )

    fig = px.line(
        trend,
        x="reported_date",
        y="count",
        color="category",
        title="Cyber Incidents Over Time"
    )
    return fig
def dataset_growth():
    df = pd.read_sql("SELECT * FROM datasets", db.conn)
    df["created_date"] = pd.to_datetime(df["created_date"])

    fig = px.histogram(
        df,
        x="created_date",
        title="Dataset Creation Over Time"
    )
    return fig
def it_ticket_trend():
    df = pd.read_sql("SELECT * FROM it_tickets", db.conn)
    df["created_date"] = pd.to_datetime(df["created_date"])

    trend = df.groupby(df["created_date"].dt.date).size().reset_index(name="tickets")

    fig = px.line(
        trend,
        x="created_date",
        y="tickets",
        title="IT Tickets Over Time"
    )
    return fig
