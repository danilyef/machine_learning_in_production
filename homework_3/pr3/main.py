import openai
import pandas as pd
import random

# OpenAI API key
openai.api_key = 'your_api_key_here'

def generate_review(product_name, sentiment):
    prompt = f"Write a short {sentiment} customer review for the product '{product_name}'."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that writes product reviews."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content'].strip()

# Generate synthetic dataset
product_name = "Iphone 10"
sentiments = ['positive', 'negative', 'neutral']
num_reviews = 100

data = []
for _ in range(num_reviews):
    sentiment = random.choice(sentiments)
    review = generate_review(product_name, sentiment)
    if sentiment == 'negative':
        rating = random.randint(1, 2)
    elif sentiment == 'neutral':
        rating = 3
    else:  # positive
        rating = random.randint(4, 5)
    data.append({'product': product_name, 'review': review, 'sentiment': sentiment, 'rating': rating})

# Create DataFrame and save to CSV
df = pd.DataFrame(data)
df.to_parquet('synthetic_reviews.parquet', index=False)
