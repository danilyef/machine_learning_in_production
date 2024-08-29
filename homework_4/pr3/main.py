import openai
import pandas as pd
import random

# OpenAI API key
openai.api_key = 'your_api_key_here'

def generate_email(category):
    categories = {
        'Bussines inquiry': 'Geschäftsanfrage',
        'Collection request': 'Inkassoanfrage',
        'Service request': 'Serviceanfrage',
        'Cancelation': 'Kündigung',
        'Billing': 'Rechnungsstellung',
        'Technical issue': 'Technisches Problem',
        'Payment method': 'Zahlungsmethode',
        'Documents': 'Dokumente',
        'Other': 'Sonstiges'
    }
    
    prompt = f"Schreiben Sie eine kurze E-Mail auf Deutsch an ein Telekommunikationsunternehmen X bezüglich einer {categories[category]}. Die E-Mail sollte realistisch sein und typische Kundenanliegen widerspiegeln."
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Sie sind ein Assistent, der realistische Kunden-E-Mails auf Deutsch verfasst."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content'].strip()

# Generate synthetic dataset
categories = [
    'Bussines inquiry', 'Collection request', 'Service request', 'Cancelation',
    'Billing', 'Technical issue', 'Payment method', 'Documents', 'Other'
]
num_emails = 100

data = []
for _ in range(num_emails):
    category = random.choice(categories)
    email_text = generate_email(category)
    data.append({'category': category, 'email_text': email_text})

# Create DataFrame and save to Parquet
df = pd.DataFrame(data)
df.to_parquet('synthetic_emails.parquet', index=False)