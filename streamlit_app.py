import streamlit as st
import pandas as pd
from PIL import Image
import os

# Initialize session state
if 'images' not in st.session_state:
    st.session_state['images'] = []

# File uploader to add images
uploaded_files = st.file_uploader("Upload Images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Capture uploaded files and add to session state
for uploaded_file in uploaded_files:
    image = Image.open(uploaded_file)
    st.session_state['images'].append({
        'image': image,
        'name': uploaded_file.name,
        'attribute_1': '',
        'attribute_2': ''
    })

# Display images and attributes input fields
st.write("### Arrange Images and Enter Attributes")
for idx, img_data in enumerate(st.session_state['images']):
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(img_data['image'], use_container_width=True)
    with col2:
        attribute_1 = st.text_input(f"Attribute 1 for {img_data['name']}", key=f"attr1_{idx}")
        attribute_2 = st.text_input(f"Attribute 2 for {img_data['name']}", key=f"attr2_{idx}")
        # Update attributes in session state
        st.session_state['images'][idx]['attribute_1'] = attribute_1
        st.session_state['images'][idx]['attribute_2'] = attribute_2

# Button to download export
if st.button("Download Export"):
    # Prepare data for export
    export_data = []
    for img_data in st.session_state['images']:
        export_data.append({
            'Image Name': img_data['name'],
            'Attribute 1': img_data['attribute_1'],
            'Attribute 2': img_data['attribute_2']
        })
    df = pd.DataFrame(export_data)
    
    # Create CSV download link
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download image arrangement as CSV",
        data=csv,
        file_name='image_arrangement.csv',
        mime='text/csv'
    )
