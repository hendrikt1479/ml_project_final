import streamlit as st
import requests
import yaml
import joblib
from PIL import Image

# Load and set images in the first place
# header_images = Image.open('assets/banner.png')
# st.image(header_images)

# Add some information about the service
st.title('Smoke Prediction')
st.subheader('Just enter variabel below then click Predict button :sunglasses:')

# Create form of input
with st.form(key = 'air_data_form'):
    # Create box for number input
    temperature = st.number_input(
        label = '1.\tEnter Temperature[C] Value:',
        min_value = -40,
        max_value = 125,
        help = 'Value range from -40 to 125'
    )

    humidity = st.number_input(
        label = '2.\tEnter Humidity[%] Value:',
        min_value = 0,
        max_value = 100,
        help = 'Value range from 0 to 100'
    )
    
    pressure = st.number_input(
        label = '3.\tEnter Pressure[hPa] Value:',
        min_value = 300,
        max_value = 1250,
        help = 'Value range from 300 to 1250'
    )

    pm1 = st.number_input(
        label = '4.\tEnter PM1.0 Value:',
        min_value = 0,
        max_value = 65535,
        help = 'Value range from 0 to 65535'
    )

    tvoc = st.number_input(
        label = '5.\tEnter TVOC[ppb] Value:',
        min_value = 0,
        max_value = 60000,
        help = 'Value range from 0 to 60000'
    )

    eco2 = st.number_input(
        label = '6.\tEnter eCO2[ppm] Value:',
        min_value = 400,
        max_value = 60000,
        help = 'Value range from 400 to 60000'
    )

    h2 = st.number_input(
        label = '7.\tEnter Raw H2 Value:',
        min_value = 0,
        max_value = 60000,
        help = 'Value range from 0 to 60000'
    )

    ethanol = st.number_input(
        label = '8.\tEnter Raw Ethanol Value:',
        min_value = 0,
        max_value = 60000,
        help = 'Value range from 0 to 60000'
    )
    
    # Create button to submit the form
    submitted = st.form_submit_button('Predict')

    # Condition when form submitted
    if submitted:
        # Create dict of all data in the form
        raw_data = {
            'Temperature': temperature,
            'Humidity': humidity,
            'Pressure': pressure,
            'PM1': pm1,
            'TVOC': tvoc,
            'eCO2': eco2,
            'H2': h2,
            'Ethanol': ethanol
        }

        # Create loading animation while predicting
        with st.spinner('Sending data to prediction server ...'):
            res = requests.post('http://api_backend:8080/predict', json = raw_data).json()
            
        # Parse the prediction result
        if res['error_msg'] != '':
            st.error('Error Occurs While Predicting: {}'.format(res['error_msg']))
        else:
            if res['res'] != 'Tidak ada api.':
                st.warning('Ada api.')
            else:
                st.success('Tidak ada api.')