import streamlit as st
import requests
import json


# =========================================================================================

st.write("""

# Malaria: Parasitized or Uninfected

""")


# ========================================================================================
st.write("""#  """)

# ========================================================================================

st.write("""### Upload an image of a cell and dectect whether it is parasitized or uninfected """)

# =========================================================================================

# ========================================================================================
st.write("""#  """)

# ========================================================================================

uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()

    with open("img.jpeg", 'wb') as f:
        f.write(bytes_data)

    st.image("img.jpeg")



# Button
predict_bt = st.button('Predict')

st.write("""# """)

# server url
url = 'https://jayem-11-malaria.hf.space/predict'  

if predict_bt:

    summary = ""

    # for file in files:
    data = {'file': open("img.jpeg", 'rb')}

    response = requests.post(url, files=data)

    # Decode the byte string to string
    str_response = response.content.decode()

    # Parse the string to JSON
    json_response = json.loads(str_response)

    # Retrieve the summary content
    pred_class = json_response['class']
    confidence = json_response['confidence']

    st.success(pred_class)


    # Call the function
    st.balloons()
