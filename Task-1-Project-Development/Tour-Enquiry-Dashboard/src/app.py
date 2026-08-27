from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "tour_enquiries.csv"

st.set_page_config(page_title="Tour Enquiry Intelligence", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["enquiry_datetime"])
    df["date"] = df["enquiry_datetime"].dt.date
    df["hour"] = df["enquiry_datetime"].dt.hour
    df["weekday"] = df["enquiry_datetime"].dt.day_name()
    return df


df = load_data()
st.title("Tour Enquiry Intelligence Dashboard")
st.caption("Explore demand timing, destination popularity, conversion and enquiry geography.")

with st.sidebar:
    st.header("Filters")
    destinations = st.multiselect("Destination", sorted(df["destination"].unique()), default=sorted(df["destination"].unique()))
    sources = st.multiselect("Lead source", sorted(df["source"].unique()), default=sorted(df["source"].unique()))
    statuses = st.multiselect("Status", sorted(df["status"].unique()), default=sorted(df["status"].unique()))

filtered = df[df["destination"].isin(destinations) & df["source"].isin(sources) & df["status"].isin(statuses)].copy()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Enquiries", f"{len(filtered):,}")
c2.metric("Bookings", f"{(filtered['status']=='Booked').sum():,}")
conversion = (filtered["status"].eq("Booked").mean()*100) if len(filtered) else 0
c3.metric("Booking rate", f"{conversion:.1f}%")
c4.metric("Median budget", f"₹{filtered['budget_inr'].median():,.0f}" if len(filtered) else "₹0")

left, right = st.columns(2)
with left:
    by_hour = filtered.groupby("hour", as_index=False).size()
    fig = px.bar(by_hour, x="hour", y="size", labels={"size":"Enquiries"}, title="Peak Enquiry Hours")
    st.plotly_chart(fig, use_container_width=True)
with right:
    by_dest = filtered.groupby("destination", as_index=False).size().sort_values("size", ascending=False)
    fig = px.bar(by_dest, x="destination", y="size", labels={"size":"Enquiries"}, title="Most Popular Destinations")
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    by_source = filtered.groupby(["source", "status"], as_index=False).size()
    fig = px.bar(by_source, x="source", y="size", color="status", barmode="stack", labels={"size":"Enquiries"}, title="Lead Funnel by Source")
    st.plotly_chart(fig, use_container_width=True)
with right:
    by_day = filtered.groupby("weekday", as_index=False).size()
    order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    by_day["weekday"] = pd.Categorical(by_day["weekday"], categories=order, ordered=True)
    by_day = by_day.sort_values("weekday")
    fig = px.line(by_day, x="weekday", y="size", markers=True, labels={"size":"Enquiries"}, title="Weekly Enquiry Pattern")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Geographic Distribution")
if len(filtered):
    st.map(filtered[["latitude", "longitude"]], latitude="latitude", longitude="longitude")
else:
    st.info("No records match the selected filters.")

st.subheader("Filtered Records")
st.dataframe(filtered.sort_values("enquiry_datetime", ascending=False), use_container_width=True)
