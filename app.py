import streamlit as st
import pandas as pd
import joblib

# PAGE CONFIGURATION
st.set_page_config(
    page_title="House Price Predictor",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# LOAD TRAINED MODEL
@st.cache_resource
def load_model():
    """Load trained model and feature list."""

    model = joblib.load("model/house_price_model.pkl")
    feature_names = joblib.load("model/model_features.pkl")

    return model, feature_names

model, feature_names = load_model()

# DATASET INFORMATION
TOTAL_HOUSES = 545
MODEL_NAME = "Linear Regression"
R2_SCORE = 0.653
MAE = "₹ 9.70 Lakhs"

# HEADER
st.title("🏡 House Price Predictor")
st.write("""Estimate residential property prices instantly using a trained Machine Learning model built with Linear Regression""")

st.divider()

# SIDEBAR
st.sidebar.header("Property Details")
st.sidebar.caption("Enter the property information below.")
st.sidebar.divider()

# PROPERTY SIZE
st.sidebar.subheader("Property Size")

area = st.sidebar.number_input(
    "Area (sq ft)",
    min_value=1000,
    max_value=20000,
    value=5000,
    step=100
)

bedrooms = st.sidebar.slider(
    "Bedrooms",
    min_value=1,
    max_value=10,
    value=3
)

bathrooms = st.sidebar.slider(
    "Bathrooms",
    min_value=1,
    max_value=10,
    value=2
)

stories = st.sidebar.slider(
    "Stories",
    min_value=1,
    max_value=4,
    value=2
)

parking = st.sidebar.slider(
    "Parking Spaces",
    min_value=0,
    max_value=5,
    value=1
)

st.sidebar.divider()
# PROPERTY FEATURES
st.sidebar.subheader("Property Features")

mainroad = st.sidebar.toggle(
    "Main Road Access",
    value=True
)

guestroom = st.sidebar.toggle(
    "Guest Room",
    value=False
)

basement = st.sidebar.toggle(
    "Basement",
    value=False
)

hotwaterheating = st.sidebar.toggle(
    "Hot Water Heating",
    value=False
)

airconditioning = st.sidebar.toggle(
    "Air Conditioning",
    value=True
)

prefarea = st.sidebar.toggle(
    "Preferred Area",
    value=False
)

st.sidebar.divider()
# FURNISHING
st.sidebar.subheader("Furnishing")

furnishing = st.sidebar.radio(
    "Select Furnishing Status",
    (
        "Furnished",
        "Semi-Furnished",
        "Unfurnished"
    )
)

st.sidebar.divider()

# ENCODE INPUTS
mainroad = int(mainroad)
guestroom = int(guestroom)
basement = int(basement)
hotwaterheating = int(hotwaterheating)
airconditioning = int(airconditioning)
prefarea = int(prefarea)

furnishingstatus_semi_furnished = 0
furnishingstatus_unfurnished = 0

if furnishing == "Semi-Furnished":
    furnishingstatus_semi_furnished = 1

elif furnishing == "Unfurnished":
    furnishingstatus_unfurnished = 1

# CREATE INPUT DATAFRAME
input_data = pd.DataFrame({

    "area": [area],
    "bedrooms": [bedrooms],
    "bathrooms": [bathrooms],
    "stories": [stories],
    "mainroad": [mainroad],
    "guestroom": [guestroom],
    "basement": [basement],
    "hotwaterheating": [hotwaterheating],
    "airconditioning": [airconditioning],
    "parking": [parking],
    "prefarea": [prefarea],
    "furnishingstatus_semi-furnished": [
        furnishingstatus_semi_furnished
    ],
    "furnishingstatus_unfurnished": [
        furnishingstatus_unfurnished
    ]

})

# MATCH TRAINING FEATURE ORDER
input_data = input_data[feature_names]
#Summary
left_col, right_col = st.columns(2)
with left_col:
    st.header("Property Summary")
    summary_container = st.container(border=True)
    with summary_container:
        c1, c2 = st.columns(2)

        with c1:
            st.write(f"**Area**")
            st.write(f"{area:,} sq ft")

            st.write(f"**Bedrooms**")
            st.write(bedrooms)

            st.write(f"**Bathrooms**")
            st.write(bathrooms)

            st.write(f"**Stories**")
            st.write(stories)

            st.write(f"**Parking**")
            st.write(parking)

        with c2:

            st.write(f"**Main Road**")
            st.write("Yes" if mainroad else "No")

            st.write(f"**Guestroom**")
            st.write("Yes" if guestroom else "No")

            st.write(f"**Basement**")
            st.write("Yes" if basement else "No")

            st.write(f"**Air Conditioning**")
            st.write("Yes" if airconditioning else "No")

            st.write(f"**Furnishing**")
            st.write(furnishing)

# MODEL OVERVIEW
with right_col:
    st.header("Model Overview")
    overview_container = st.container(border=True)

    with overview_container:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Algorithm")
            st.write("""Linear Regression""")

            st.divider()
            st.subheader("Training Samples")
            st.write("""545""")

            st.divider()
            st.subheader("Features")
            st.write("""13""")
        with c2:
            st.subheader("R² Score")
            st.write("""0.653""")
            st.divider()
            st.subheader("MAE")
            st.write("""₹ 9.70 Lakhs""")
            st.divider()
            st.subheader("RMSE")
            st.write("""₹ 13.25 Lakhs""")

#Predict Button
st.divider()
st.header("Price Prediction")
predict = st.button(
    "Predict Price",
    type="primary",
    use_container_width=True
)

if predict:
    prediction = model.predict(input_data)[0]
    predicted_price_lakhs = prediction / 100000
    prediction_container = st.container(border=True)

    with prediction_container:
        st.metric(
            label="Estimated Market Price",
            value=f"₹ {predicted_price_lakhs:,.2f} Lakhs"
        )
        st.progress(100)
        st.caption(
            "Prediction generated using the trained Linear Regression model."
        )

else:
    st.info(
        "Fill in the property details from the sidebar and click **Predict Price**."
    )
st.write("")

# ABOUT PROJECT
st.divider()
l, r = st.columns(2)
with l:
    st.header("About This Project")
    st.write(
        """
    This application predicts residential house prices using a Machine Learning
    Linear Regression model trained on a real-world housing dataset.
    
    The complete workflow includes:
    
    • Data Cleaning
    
    • Feature Engineering
    
    • Feature Encoding
    
    • Model Training
    
    • Model Evaluation
    
    • Real-Time Prediction
    
    The application was developed using Streamlit and Scikit-Learn as part of an
    AI & Machine Learning portfolio.
    """
    )

with r:
    st.header("Tech Stack")
    tech_container = st.container(border=True)
    with tech_container:
        l1, l2 = st.columns(2)
        with l1:
            st.subheader("Language")
            st.write("~🐍 Python")
            st.divider()
            st.subheader("Framework")
            st.write("~⚡ Streamlit")
        with l2:
            st.subheader("ML Library")
            st.write("~🧠 Scikit-Learn")
            st.divider()
            st.subheader("Deployment")
            st.write("~📊 Streamlit Cloud")

# DISCLAIMER
st.divider()
st.info(
    """
Predicted prices are generated by a Machine Learning model trained on historical
housing data. Results are intended for educational and demonstration purposes.
"""
)

# FOOTER
st.divider()
footer_left, footer_right = st.columns([3,1])

with footer_left:
    st.caption(
        "Built with ❤️ using Python, Streamlit, Pandas and Scikit-Learn."
    )

with footer_right:
    st.caption("Version 1.0")