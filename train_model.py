import json
import pickle
import random

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load dataset
with open("intents.json", "r", encoding="utf-8") as file:
    data = json.load(file)

sentences = []
labels = []

# Prepare training data
for intent in data["intents"]:
    for pattern in intent["patterns"]:
        if pattern.strip():
            sentences.append(pattern)
            labels.append(intent["tag"])

# Convert text into numerical features
vectorizer = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2)
)

X = vectorizer.fit_transform(sentences)

# Train classification model
model = LogisticRegression(
    max_iter=1000
)

model.fit(X, labels)

# Save trained model
with open("chatbot_model.pkl", "wb") as file:
    pickle.dump(model, file)

# Save vectorizer
with open("vectorizer.pkl", "wb") as file:
    pickle.dump(vectorizer, file)

print("Model trained successfully!")
print("Training sentences:", len(sentences))
print("Number of intents:", len(set(labels)))