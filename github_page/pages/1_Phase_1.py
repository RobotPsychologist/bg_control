import streamlit as st

st.title("Phase 1 - Meal Identification")
st.write("Meal Identification develop the ability to identify unlabelled meals in time series BG data. The goal of this project is to be able to identify the top 'n' most significant meals of a PWD per day from continuous glucose monitor data alone. The time series detection models are evaluated on various metrics that measure the proximity of the identified meal regions or change poitns to ground truth labels. ")