import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score

# Load the enhanced dataset
df = pd.read_csv('enhanced_expense_data.csv')

print(f"Total records: {len(df)}")
print(f"\nOriginal categories: {df['category'].nunique()}")

# Filter out categories with fewer than 10 samples
category_counts = df['category'].value_counts()
valid_categories = category_counts[category_counts >= 10].index
df = df[df['category'].isin(valid_categories)]

print(f"After filtering (min 10 samples per category): {len(df)} records")
print(f"Categories used: {df['category'].nunique()}")
print(f"\nCategory distribution:\n{df['category'].value_counts()}")

# Prepare features (description) and target (category)
X = df['description']
y = df['category']

# Split data: 80% train, 20% test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Create ML pipeline: TF-IDF vectorizer + Naive Bayes classifier
model_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=100)),
    ('classifier', MultinomialNB())
])

# Train the model
print("\nTraining the model...")
model_pipeline.fit(X_train, y_train)

# Make predictions
y_pred = model_pipeline.predict(X_test)

# Evaluate
accuracy = accuracy_score(y_test, y_pred)
print(f"\nModel Accuracy: {accuracy * 100:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

# Save the trained model
with open('expense_classifier_model.pkl', 'wb') as f:
    pickle.dump(model_pipeline, f)

print("\nModel saved as 'expense_classifier_model.pkl'")

# Test with sample predictions
print("\n--- Sample Predictions ---")
test_descriptions = [
    "Starbucks Coffee",
    "Uber ride downtown",
    "Whole Foods groceries",
    "Pizza Hut delivery"
]

for desc in test_descriptions:
    prediction = model_pipeline.predict([desc])[0]
    print(f"'{desc}' -> {prediction}")