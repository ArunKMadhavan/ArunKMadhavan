import streamlit as st
import cv2
from ultralytics import YOLO
import random
import time

from genai_sugg import generate_suggestion

# Load YOLOv8 model
model = YOLO('/Users/arunkumarmadhavannair/Downloads/yolov9_filtered_fruits/weights/best.pt')

# List of class names corresponding to the indices
class_names = [
    'tomato', 'broccoli', 'banana', 'lemon', 'cucumber'
]
# Initialize session state for captured items
if 'captured_items' not in st.session_state:
    st.session_state.captured_items = {}

if 'tips_cache' not in st.session_state:
    st.session_state.tips_cache = {}

if 'last_item_name' not in st.session_state:
    st.session_state.last_item_name = None

# Set up Streamlit layout with custom styling
st.set_page_config(page_title="NexGen SmartShop Culinary", layout="wide")
st.markdown(
    """
    <style>
    /* Custom CSS for Streamlit */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

    body {
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        color: #e6e6e6;
        font-family: 'Montserrat', sans-serif;
    }
    .main-title {
        font-size: 48px;
        color: #ecf0f1;
        text-align: center;
        font-weight: bold;
        padding-bottom: 20px;
        text-shadow: 2px 2px 4px #34495e;
        animation: fadeIn 1s ease-in-out;
    }
    .sidebar .sidebar-content {
        background: rgba(255, 255, 255, 0.1);
        padding: 10px;
        border-radius: 15px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    .info-box {
        padding: 20px;
        border: 2px solid #2980b9;
        border-radius: 15px;
        background: rgba(44, 62, 80, 0.8);
        font-size: 20px;
        color: #ecf0f1;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        animation: slideUp 0.5s ease-in-out;
    }
    .info-box strong {
        color: #ffffff;
    }
    .scan-feedback {
        font-size: 28px;
        font-weight: bold;
        color: #2980b9;
        text-align: center;
        margin-top: 20px;
        animation: pulse 1s infinite, fadeIn 1s ease-in-out;
    }
    .footer {
        text-align: center;
        font-size: 14px;
        color: #ecf0f1;
        padding-top: 20px;
    }
    /* Custom CSS for the sections */
    .section {
        padding: 20px;
        border-radius: 15px;
        margin-top: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        background: linear-gradient(135deg, #2c3e50, #34495e);
        color: #ffffff;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .section:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
    }
    .section h3 {
        font-size: 24px;
        font-weight: 600;
        margin-bottom: 15px;
        color: #ecf0f1;
        border-bottom: 2px solid #3498db;
        padding-bottom: 10px;
    }
    .section p {
        font-size: 18px;
        line-height: 1.6;
    }
    .item-list {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    .item-list li {
        background-color: #2c3e50;
        padding: 15px;
        margin-bottom: 10px;
        border-radius: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .item-list li:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
        background-color: #34495e;
    }
    .item-list li span {
        font-weight: 500;
        font-size: 18px;
        color: #f0f0f0; /* Lighter font color for better readability */
    }
    .item-list li .price {
        color: #1abc9c;
        font-weight: bold;
        font-size: 18px;
    }
    .recipe-section {
        background: linear-gradient(135deg, #27ae60, #2ecc71);
    }
    .nutrition-section {
        background: linear-gradient(135deg, #8e44ad, #9b59b6);
    }
    .nutrition-section.full-width {
        width: 100%;
        margin: 0 auto;
    }
    /* Styling for links in the nutrition section */
    .nutrition-section a {
        color: #1abc9c;
        font-weight: bold;
        text-decoration: underline;
        transition: color 0.3s ease;
    }
    .nutrition-section a:hover {
        color: #16a085;
    }
    .cart-section {
        background: linear-gradient(135deg, #2c3e50, #1c2833);
        border: 2px solid #1abc9c;
        border-radius: 15px;
        padding: 20px;
    }
    .webcam-section {
    background: linear-gradient(135deg, #2c3e50, #1c2833);
    border: 2px solid #3498db;
    border-radius: 15px;
    padding: 0;
    margin-bottom: 20px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 640px; /* Adjust the width to fit the webcam feed */
    height: auto;
}

.webcam-title {
    font-size: 24px;
    font-weight: bold;
    text-align: center;
    padding: 10px 0;
    background-color: rgba(0, 0, 0, 0.5);
    color: #ecf0f1;
    width: 100%;
    border-bottom: 2px solid #3498db;
}

.webcam-feed {
    width: 800px; /* Set the width to match the webcam feed */
    height: auto;
    object-fit: cover;
    border-radius: 0 0 15px 15px;
}
 .sidebar .dropdown-container {
        background: #34495e;
        padding: 10px 15px;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        transition: background 0.3s ease, box-shadow 0.3s ease;
    }

    .sidebar .dropdown-container:hover {
        background: #2c3e50;
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.4);
    }

    .sidebar .stSelectbox label {
        font-size: 18px;
        font-weight: 600;
        color: #ecf0f1;
    }

    .sidebar .stSelectbox div[data-baseweb="select"] {
        background: #2c3e50;
        border-radius: 10px;
        padding: 10px;
        color: #ecf0f1;
    }

    .sidebar .stSelectbox div[data-baseweb="select"] .css-1n8i4of {
        color: #1abc9c;
    }

    .sidebar .stSelectbox div[data-baseweb="select"] .css-1wa3eu0-placeholder {
        color: #95a5a6;
    }

    .sidebar .stSelectbox div[data-baseweb="select"]:hover {
        background: #2ecc71;
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar for additional controls with interactive elements
st.sidebar.title("Settings")
confidence_threshold = st.sidebar.slider("Confidence Threshold", 0.1, 1.0, 0.6, 0.05)
st.sidebar.markdown("Use the controls to fine-tune the scanning process.")

# Sidebar title
st.sidebar.title("Choose Suggestion Type")

# Define the options for the dropdown
options = ["FreshGuard", "Nutrient Insights", "EcoWise", "Perfect Pairings", "Meal Master"]

# Create a custom dropdown in the sidebar
st.sidebar.markdown('<div class="dropdown-container">', unsafe_allow_html=True)
suggestion_type = st.sidebar.selectbox(
    "",
    options=options,
    index=options.index(st.session_state.get('selected_option', options[0]))
)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Update session state with the selected option
st.session_state.suggestion_type = suggestion_type

# Main title with branding
st.markdown("<h1 class='main-title'> 🍽️ NexGen SmartShop Culinary 🍽️ </h1>", unsafe_allow_html=True)

# Create two columns for the layout
col1, col2 = st.columns([2, 1])

# Initialize a dictionary to store captured items
captured_items = {}
last_detected_items = set()


# Mock function to get weight and price
def get_weight_and_price(label):
    weight = round(random.uniform(0.1, 1.5), 2)  # Mock weight in kg
    price = round(weight * 3.0, 2)  # Mock price calculation (e.g., $3/kg)
    return weight, price


# Start video capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 645)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 0)

# Streamlit real-time video
with col1:
    st.markdown("<div class='webcam-section'><div class='webcam-title'>📷 Identify your Item</div>",
                unsafe_allow_html=True)
    frame_placeholder = st.empty()
    st.markdown("</div>", unsafe_allow_html=True)

list_placeholder = col2.empty()  # Placeholder for the stylish list

# Display recipe recommendations in the right column
with col2:
    recipe_section = st.empty()

# Display the nutritional values outside the columns, spanning the full width
nutrition_section = st.empty()


def get_or_generate_tips(item_name, suggestion_type):
    # Check if the tips for the current item and suggestion type are already cached
    if (item_name in st.session_state.tips_cache and
            suggestion_type in st.session_state.tips_cache[item_name]):
        return st.session_state.tips_cache[item_name][suggestion_type]

    # Generate new tips if not cached
    with st.spinner('Let me suggest you few tips...'):
        if suggestion_type == "FreshGuard":
            tips = generate_suggestion([item_name], suggestion_type="storage")
        elif suggestion_type == "Nutrient Insights":
            tips = generate_suggestion([item_name], suggestion_type="nutritional")
        elif suggestion_type == "EcoWise":
            tips = generate_suggestion([item_name], suggestion_type="sustainability")
        elif suggestion_type == "Perfect Pairings":
            tips = generate_suggestion([item_name], suggestion_type="pairing")
        elif suggestion_type == "Meal Master":
            tips = generate_suggestion([item_name], suggestion_type="mealplan")

        # Cache the generated tips
        if item_name not in st.session_state.tips_cache:
            st.session_state.tips_cache[item_name] = {}
        st.session_state.tips_cache[item_name][suggestion_type] = tips

    return tips

while True:
    ret, frame = cap.read()

    if not ret:
        st.error("Failed to capture video.")
        break

    # Simulate scanning delay
    time.sleep(0.2)

    # Detect and track objects
    results = model.track(frame, persist=False, conf=confidence_threshold)

    # Plot results on the frame
    frame_ = results[0].plot()

    # Flag to check if any new items are detected
    new_item_detected = False

    # Check detected classes and update their weight and price
    for result in results:
        for box in result.boxes:
            label_idx = int(box.cls.item())  # Convert tensor to Python int
            label_name = class_names[label_idx] if label_idx < len(class_names) else "Unknown"

            # Get mock weight and price for detected class
            weight, price = get_weight_and_price(label_name)

            # Check if the item is new
            if label_name not in st.session_state.captured_items:
                new_item_detected = True
                st.session_state.captured_items[label_name] = {'Weight': weight, 'Price': price}
                #st.rerun()  # Force a rerun to show the spinner and process the new item

    # Display the frozen frame in Streamlit
    frame_placeholder.image(frame_, channels="BGR")
    # Prepare the stylish list content
    # Prepare the stylish list content
    cart_section = """
    <div class='section cart-section'>
        <h3>🛒 Your Shopping Cart</h3>
        <ul class='item-list'>
    """

    for label_name, details in st.session_state.captured_items.items():
        price = details['Price']
        cart_section += f"<li><span>{label_name}</span><span class='price'>${price:.2f}</span></li>"

    cart_section += """</ul></div>"""

    # Display the visually appealing cart section
    list_placeholder.markdown(cart_section, unsafe_allow_html=True)

    # Update the last detected item name
    if new_item_detected:
        st.session_state.last_item_name = list(st.session_state.captured_items.keys())[-1]


    # Ensure last_item_name is valid and proceed to generate or fetch suggestions
    if st.session_state.last_item_name:
        seasonal_tips = get_or_generate_tips(st.session_state.last_item_name, suggestion_type)

        # Display the suggestion
        nutrition_section.markdown(
            f"""
               <div class='section nutrition-section full-width'>
                   <h3>🌱 Smart Suggestions for you</h3>
                   {seasonal_tips}
               </div>
               """,
            unsafe_allow_html=True
        )


# Footer branding
st.markdown("<div class='footer'>© 2024 Best of us - rrrr. All rights reserved.</div>", unsafe_allow_html=True)

# Release resources
cap.release()
cv2.destroyAllWindows()
