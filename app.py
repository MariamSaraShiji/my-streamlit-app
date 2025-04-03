import streamlit as st
import pandas as pd
import numpy as np
import random
from faker import Faker
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import cv2
import os
from PIL import Image

import streamlit as st
import base64

# Function to set an image (JPG, PNG) as background
def set_bg_image(file_path):
    with open(file_path, "rb") as f:
        data = base64.b64encode(f.read()).decode()

    file_ext = file_path.split(".")[-1]  # Get file extension

    bg_style = f"""
    <style>
    .stApp {{
        background: url("data:image/{file_ext};base64,{data}");
        background-size: contain;  /* Change 'contain' to 'cover' if needed */
        background-repeat: no-repeat;
        background-position: center;
        background-attachment: fixed;
    }}
    
    .title {{
        color: white;
        text-align: center;
        font-size: 50px;
        font-weight: bold;
    }}
    </style>
    """
    st.markdown(bg_style, unsafe_allow_html=True)


# Call the function with your image file
set_bg_image("C:/CHRIST/3rd sem/Advanced Python/ETE 3/images/lmao.jpg")  # Change to your image path




# Generate  Dataset
def generate_dataset():
    fake = Faker()
    tracks = ["AI & ML", "Cybersecurity", "IoT", "Blockchain"]
    states = ["Kerala", "Tamil Nadu", "Karnataka", "Maharashtra"]
    colleges = ["IIT Madras", "NIT Trichy", "VIT Vellore", "CET Trivandrum"]
    
    data = []
    for _ in range(400):
        participant = {
            "Participant Name": fake.name(),
            "Track": random.choice(tracks),
            "Day": random.randint(1, 4),
            "College": random.choice(colleges),
            "State": random.choice(states),
            "Feedback": fake.sentence()
        }
        data.append(participant)
    
    df = pd.DataFrame(data)
    df.to_csv("poster_presentation_data.csv", index=False)
    return df

# Load or Generate Dataset
try:
    df = pd.read_csv("poster_presentation_data.csv")
except:
    df = generate_dataset()

# Streamlit App
st.title("National Poster Presentation Dashboard")

# Sidebar Filters
# Custom CSS to make the sidebar black
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            background-color: black;
        }
        [data-testid="stSidebar"] * {
            color: white;  /* Makes text white for visibility */
        }
    </style>
    """,
    unsafe_allow_html=True
)


track_filter = st.sidebar.multiselect("Select Tracks", df["Track"].unique(), default=df["Track"].unique())
day_filter = st.sidebar.multiselect("Select Days", df["Day"].unique(), default=df["Day"].unique())
state_filter = st.sidebar.multiselect("Select States", df["State"].unique(), default=df["State"].unique())
college_filter = st.sidebar.multiselect("Select Colleges", df["College"].unique(), default=df["College"].unique())

# Apply all filters
filtered_df = df[
    df["Track"].isin(track_filter) &
    df["Day"].isin(day_filter) &
    df["State"].isin(state_filter) &
    df["College"].isin(college_filter)
]

st.write("### Filtered Dataset")
st.dataframe(filtered_df)



# Display small GIF at the bottom of the sidebar
gif_url = "C:/CHRIST/3rd sem/Advanced Python/ETE 3/images\pp.gif"  # Replace with your own GIF URL
st.sidebar.image(gif_url, use_container_width=True)

# Visualization - Participation Trends
st.write("### Participation Trends")
fig, ax = plt.subplots(2, 3, figsize=(18, 10))

# Count Plot
sns.countplot(x="Track", data=filtered_df, ax=ax[0, 0], palette="viridis")
ax[0, 0].set_title("Track-wise Participation")

# Pie Chart
track_counts = filtered_df["Track"].value_counts()
ax[0, 1].pie(track_counts, labels=track_counts.index, autopct='%1.1f%%', colors=sns.color_palette("plasma"))
ax[0, 1].set_title("Track-wise Distribution (Pie Chart)")

# Line Graph
state_counts = filtered_df["State"].value_counts()
ax[0, 2].plot(state_counts.index, state_counts.values, marker='o', linestyle='-', color='b')
ax[0, 2].set_title("State-wise Participation")
ax[0, 2].set_xlabel("State")
ax[0, 2].set_ylabel("Count")

# Histogram
sns.histplot(filtered_df["Day"], bins=4, kde=True, ax=ax[1, 0], color="orange")
ax[1, 0].set_title("Day-wise Distribution")

# Box Plot
sns.boxplot(x="Track", y="Day", data=filtered_df, ax=ax[1, 1], palette="muted")
ax[1, 1].set_title("Track vs. Day Distribution")

# Additional Bar Graph for College-wise Participation
sns.barplot(x=filtered_df["College"].value_counts().index, y=filtered_df["College"].value_counts().values, ax=ax[1, 2], palette="pastel")
ax[1, 2].set_title("College-wise Participation")

fig.tight_layout()
st.pyplot(fig)
# Word Cloud - Feedback Analysis
st.write("### Word Cloud for Feedback")
feedback_text = " ".join(filtered_df["Feedback"].astype(str))
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(feedback_text)
st.image(wordcloud.to_array())



# Image Processing - Day-wise Image Gallery
st.write("### Day-wise Image Gallery")

img_folder = "images"  # Ensure this folder contains images
if os.path.exists(img_folder):
    img_files = os.listdir(img_folder)

    # Extract available days from filenames (assuming naming convention "DayX_...")
    available_days = sorted(set(f.split('_')[0] for f in img_files if f.startswith("Day")))

    if available_days:
        selected_day = st.selectbox("Select Day", available_days)

        # Filter images based on selected day
        daywise_images = [img for img in img_files if img.startswith(selected_day)]
        
        if daywise_images:
            st.write(f"Images for **{selected_day}**")
            for img_file in daywise_images:
                img_path = os.path.join(img_folder, img_file)
                image = Image.open(img_path)
                st.image(image, caption=os.path.splitext(img_file)[0], use_container_width=True)
        else:
            st.write(f"No images found for {selected_day}")
    else:
        st.write("No day-specific images found in the folder.")
else:
    st.write("No images found! Please add some track-related images to the 'images' folder.")

# Custom Image Processing Component
st.write("###  Image Processing Section")

processing_option = st.selectbox("Choose Image Processing Effect", ["Grayscale", "Edge Detection", "Blur"])

if os.path.exists(img_folder) and img_files:
    img_path = os.path.join(img_folder, img_files[0])  # Process the first image
    image = cv2.imread(img_path)
    
    if image is not None:
        if processing_option == "Grayscale":
            processed_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            st.image(processed_image, use_container_width=True, channels="GRAY")
        elif processing_option == "Edge Detection":
            processed_image = cv2.Canny(image, 100, 200)
            st.image(processed_image, use_container_width=True)
        elif processing_option == "Blur":
            processed_image = cv2.GaussianBlur(image, (15, 15), 0)
            st.image(processed_image, use_container_width=True)
    else:
        st.write("Error: Unable to load the image for processing.")
else:
    st.write("No images found for processing.")
