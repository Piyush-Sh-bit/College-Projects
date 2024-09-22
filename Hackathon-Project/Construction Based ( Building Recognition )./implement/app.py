import os
import numpy as np
import streamlit as st
import tensorflow as tf
from tensorflow.keras.models import load_model, Sequential
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from skimage.metrics import structural_similarity as ssim
import cv2
import matplotlib.pyplot as plt
from io import BytesIO
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# Define constants
IMAGE_SIZE = (224, 224)  # Must match the size used during training
MODEL_PATH = r'C:\Users\piyus\Downloads\hope\building_completion_model_enhanced.h5'  # Path to your saved model

# Load the model for Code 2 once at the start
completion_model = load_model(MODEL_PATH)

# Load the model for Code 1
def load_comparison_model():
    base_model = tf.keras.applications.MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
    base_model.trainable = False

    model = Sequential([
        base_model,
        GlobalAveragePooling2D(),
        Dense(256, activation='relu'),
        Dropout(0.5),
        Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    return model

comparison_model = load_comparison_model()

# Function to preprocess the image (for Code 2)
def load_and_preprocess_image(image):
    img = load_img(image, target_size=IMAGE_SIZE)
    img_array = img_to_array(img)
    img_array = preprocess_input(img_array)
    return np.expand_dims(img_array, axis=0)

# Function to predict completion percentage (Code 2)
def predict_completion(image):
    processed_image = load_and_preprocess_image(image)
    prediction = completion_model.predict(processed_image)[0][0]
    return prediction

# Function to classify images (from Code 1)
def classify_image(image, model):
    img = load_img(image, target_size=(224, 224))
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, 0)
    prediction = model.predict(img_array)[0][0]
    class_name = "Developed" if prediction > 0.5 else "Underdeveloped"
    confidence = abs(prediction - 0.5) * 200
    return class_name, confidence, prediction

# Function to categorize progress based on percentage
def categorize_progress(percentage):
    if percentage <= 30:
        return "Incomplete"
    elif 30 < percentage <= 70:
        return "Underdevelopment"
    else:
        return "Developed"

# Streamlit app
def main():
    st.title('Construction Activity and Completion Assessment')

    st.sidebar.header('Upload Images')
    uploaded_img1 = st.sidebar.file_uploader("Upload Image 1", type=["png", "jpg", "jpeg"])
    uploaded_img2 = st.sidebar.file_uploader("Upload Image 2 (for comparison)", type=["png", "jpg", "jpeg"])

    if uploaded_img1 and uploaded_img2:
        # --- Perform image comparison (Code 1) ---
        # Save uploaded images temporarily
        with open("temp_img1.png", "wb") as f:
            f.write(uploaded_img1.getbuffer())
        with open("temp_img2.png", "wb") as f:
            f.write(uploaded_img2.getbuffer())

        img1_class, img1_conf, img1_pred = classify_image("temp_img1.png", comparison_model)
        img2_class, img2_conf, img2_pred = classify_image("temp_img2.png", comparison_model)

        # Compare construction progress
        img1_array = img_to_array(load_img("temp_img1.png", target_size=(224, 224)))
        img2_array = img_to_array(load_img("temp_img2.png", target_size=(224, 224)))

        img1_gray = cv2.cvtColor(img1_array, cv2.COLOR_RGB2GRAY)
        img2_gray = cv2.cvtColor(img2_array, cv2.COLOR_RGB2GRAY)

        if img1_gray.max() - img1_gray.min() == 255:
            data_range = 255
        else:
            data_range = img1_gray.max() - img1_gray.min()

        similarity_index, _ = ssim(img1_gray, img2_gray, data_range=data_range, full=True)

        if img1_class == img2_class:
            st.write(f"Structural Similarity Index: {similarity_index:.2f}")
            if similarity_index > 0.8:
                st.write("The images are very similar, suggesting little to no progress between them.")
            else:
                st.write("The images show some differences, suggesting some progress or changes.")
        else:
            developed_confidence = img1_conf if img1_class == "Developed" else img2_conf
            underdeveloped_confidence = img2_conf if img1_class == "Developed" else img1_conf
            progress = (underdeveloped_confidence / developed_confidence) * 100
            underdeveloped_image = "Image 2" if img1_class == "Developed" else "Image 1"
            st.write(f"{underdeveloped_image} (Underdeveloped) is approximately {progress:.2f}% complete compared to the Developed image.")
        
        # Calculate overall progress based on model predictions
        overall_progress = (img1_pred + img2_pred) / 2 * 100
        st.write(f"Overall estimated progress of the construction site: {overall_progress:.2f}%")
        progress_category = categorize_progress(overall_progress)
        st.write(f"Category based on progress: {progress_category}")

        # Plot comparison results
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        
        ax1.imshow(img1_array / 255.0)
        ax1.set_title(f"Confidence: {img1_conf:.2f}%")
        ax1.axis('off')
        
        ax2.imshow(img2_array / 255.0)
        ax2.set_title(f"Confidence: {img2_conf:.2f}%")
        ax2.axis('off')
        
        plt.suptitle(f"Construction Progress Comparison: {overall_progress:.2f}%\n", fontsize=16)
        st.pyplot(fig)

        # --- Perform building completion prediction (Code 2) ---
        if st.button("Predict Completion for Both Images"):
            try:
                # Predict completion for Image 1
                completion_percentage_img1 = predict_completion("temp_img1.png") * 100
                completion_category_img1 = categorize_progress(completion_percentage_img1)
                st.success(f"Predicted completion for Image 1: {completion_percentage_img1:.2f}% ({completion_category_img1})")

                # Predict completion for Image 2
                completion_percentage_img2 = predict_completion("temp_img2.png") * 100
                completion_category_img2 = categorize_progress(completion_percentage_img2)
                st.success(f"Predicted completion for Image 2: {completion_percentage_img2:.2f}% ({completion_category_img2})")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    elif uploaded_img1 or uploaded_img2:
        st.error("Please upload both images for comparison.")
    
    else:
        st.warning("Upload images to proceed.")

if __name__ == "__main__":
    main()
