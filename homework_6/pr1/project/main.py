from processing import clean_text
from model import load_model, predict

def main():
    # Step 1: Load the model
    model = load_model()

    # Step 2: Get input text
    input_text = input("Enter the text to classify: ")

    # Step 3: Clean the text
    cleaned_text = clean_text(input_text)

    # Step 4: Make prediction
    prediction = predict(model, cleaned_text)

    # Step 5: Output result
    print(f"The predicted class is: {prediction}")

if __name__ == "__main__":
    main()
