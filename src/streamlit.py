import streamlit as st
import requests
import yaml
import joblib
import json
from PIL import Image

# Add some information about the service
st.info("# Prediksi Kebakaran :fire:")

col1, col2 = st.columns(2)
header_images = Image.open("images/images.jpg")
col1.image(header_images)

col2.success("##### Project ML Process")
col2.error("""
Hendrik Tanaka  
Pacmann-Desember 2022
""")
    





with st.form(key = "kebakaran_form"):
    col1, col2, col3 = st.columns(3)
    # Create box for number input
    temperature = col1.number_input(
        label = "Temperature [C] :",
        step = 1
        # min_value = -40,
        # max_value = 125,
        # help = "Value range from -40 to 125"
    )

    humidity = col1.number_input(
        label = "Humidity [%] :",
        step = 1
        # min_value = 0,
        # max_value = 100,
        # help = "Value range from 0 to 100"
    )

    tvoc = col1.number_input(
        label = "TVOC [ppb] :",
        step = 1
        # min_value = 0,
        # max_value = 60000,
        # help = "Value range from 0 to 60000"
    )

    eco2 = col2.number_input(
        label = "eCO2 [ppm] :",
        step = 1
        # min_value = 400,
        # max_value = 60000,
        # help = "Value range from 400 to 60000"
    )

    h2 = col2.number_input(
        label = "Raw H2 :",
        step = 1
        # min_value = 0,
        # max_value = 60000,
        # help = "Value range from 0 to 60000"
    )

    ethanol = col2.number_input(
        label = "Raw Ethanol :",
        step = 1
        # min_value = 0,
        # max_value = 60000,
        # help = "Value range from 0 to 60000"
    )

    pressure = col3.number_input(
        label = "Pressure [hPa] :",
        step = 1
        # min_value = 300,
        # max_value = 1250,
        # help = "Value range from 300 to 1250"
    )

    pm1 = col3.number_input(
        label = "PM1.0 :",
        step = 1
        # min_value = 0,
        # max_value = 65535,
        # help = "Value range from 0 to 65535"
    )



    # Create button to submit the form
    submitted = col3.form_submit_button("Predict")


    # Condition when form submitted
    if submitted:
        # Create dict of all data in the form
        raw_data = {
            "Temperature": temperature,
            "Humidity": humidity,
            "Pressure": pressure,
            "PM1": pm1,
            "TVOC": tvoc,
            "eCO2": eco2,
            "H2": h2,
            "Ethanol": ethanol
        }

        # Create loading animation while predicting
        with st.spinner("Mengirim data ke server ..."):
            result = requests.post("http://localhost:8080/predict/", json = raw_data)
            result = result.json()

           
            
            
        # Parse the prediction result
        # if res["error_msg"] != "":
        #     st.error("Error saat memprediksi: {}".format(res["error_msg"]))
        # else:
        #     if res["res"] == "Tidak ada api.":
        #         st.warning("Ada api-streamlit.")
        #     else:
        #         st.success("Tidak ada api-streamlit.")

            # if res["res"] == 0:
            #     st.warning("Ada api-streamlit.")
            # else:
            #     st.success("Tidak ada api-streamlit.")
            
        st.success(result)
