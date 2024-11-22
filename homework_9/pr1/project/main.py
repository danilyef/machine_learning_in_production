import streamlit as st
from utils import Model


model = Model(tokenizer_name="distilbert-base-uncased-finetuned-sst-2-english", model_name="distilbert-base-uncased-finetuned-sst-2-english")

# Create the Streamlit app title
st.title('Sentiment Analysis with DistilBERT')

# Create a text input for user's sentence
user_input = st.text_area("Enter text to analyze:", "I love this app!")

# Create analyze button
analyze_button = st.button("Analyze Sentiment")

# Make prediction when button is clicked
if analyze_button and user_input:
    # Get the prediction
    label = model.predict(user_input)
    probabilities = model.predict_proba(user_input)
    
    # Get probability score for predicted class
    score = probabilities[1] if label == "POSITIVE" else probabilities[0]

    # Display results
    st.write("### Results:")
    label_color = "green" if label == "POSITIVE" else "red"
    st.markdown(f"Label: **:{label_color}[{label}]**")
    st.write(f"Confidence: **{score:.4f}** ({score*100:.2f}%)")

    # Create a progress bar for the confidence score
    st.progress(score)