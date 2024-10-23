from processing import clean_text
from model import load_model, predict

def main():

    model = load_model()

    input_text = input("Enter the text to classify: ")

    cleaned_text = clean_text(input_text)

    prediction = predict(model, cleaned_text)

    print(f"The predicted class is: {prediction}")

if __name__ == "__main__":
    main()
