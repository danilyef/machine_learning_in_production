import requests

text = "The movie was great!"

response = requests.post("http://127.0.0.1:8000/", json=text)
sentiment = response.text

print(sentiment)