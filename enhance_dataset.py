import pandas as pd
import random

# Load the dataset
df = pd.read_csv('11 march 2025.csv')

# Define realistic transaction descriptions for each category
descriptions = {
    'Restuarant': [
        'Chipotle Mexican Grill',
        'McDonald\'s',
        'Subway Sandwiches',
        'Pizza Hut',
        'Taco Bell',
        'Olive Garden',
        'Panera Bread',
        'Five Guys Burgers',
        'Chick-fil-A',
        'Buffalo Wild Wings',
        'Red Lobster',
        'Applebee\'s',
        'Domino\'s Pizza',
        'KFC',
        'Wendy\'s'
    ],
    'Market': [
        'Whole Foods Market',
        'Trader Joe\'s',
        'Walmart Grocery',
        'Target',
        'Safeway',
        'Kroger',
        'Costco Wholesale',
        'Publix Super Market',
        'Stop & Shop',
        'Giant Food',
        'Aldi',
        'Wegmans',
        'Food Lion',
        'H-E-B',
        'Sprouts Farmers Market'
    ],
    'Coffe': [
        'Starbucks',
        'Dunkin\' Donuts',
        'Peet\'s Coffee',
        'The Coffee Bean',
        'Blue Bottle Coffee',
        'Philz Coffee',
        'Dutch Bros Coffee',
        'Caribou Coffee',
        'Tim Hortons',
        'Local Coffee Shop',
        'Cafe Nero',
        'Costa Coffee',
        'Intelligentsia Coffee'
    ],
    'Transport': [
        'Uber',
        'Lyft',
        'Yellow Cab',
        'Metro Card',
        'Gas Station - Shell',
        'Gas Station - Chevron',
        'Gas Station - BP',
        'Parking Garage',
        'Toll Road',
        'City Bus Pass',
        'Train Ticket',
        'Airport Shuttle'
    ]
}

# Add description column
def get_description(category):
    if category in descriptions:
        return random.choice(descriptions[category])
    return 'Unknown Transaction'

df['description'] = df['category'].apply(get_description)

# Reorder columns: date, description, amount, category
df = df[['date', 'description', 'amount', 'category']]

# Save enhanced dataset
df.to_csv('enhanced_expense_data.csv', index=False)

print("Dataset enhanced successfully!")
print(f"Total records: {len(df)}")
print("\nSample data:")
print(df.head(10))
print("\nCategory distribution:")
print(df['category'].value_counts())