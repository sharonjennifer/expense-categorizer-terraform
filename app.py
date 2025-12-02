from flask import Flask, request, render_template, send_file
import pandas as pd
import pickle
import os
from datetime import datetime

app = Flask(__name__)

# Load the trained model
with open('expense_classifier_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Create uploads folder
os.makedirs('uploads', exist_ok=True)
os.makedirs('results', exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return "No file uploaded", 400
    
    file = request.files['file']
    
    if file.filename == '':
        return "No file selected", 400
    
    if file and file.filename.endswith('.csv'):
        # Save uploaded file
        filepath = os.path.join('uploads', file.filename)
        file.save(filepath)
        
        # Read CSV
        df = pd.read_csv(filepath)
        
        # Check if required columns exist
        if 'description' not in df.columns:
            return "CSV must have a 'description' column", 400
        
        # Make predictions
        df['predicted_category'] = model.predict(df['description'])
        
        # Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        result_filename = f'categorized_expenses_{timestamp}.csv'
        result_path = os.path.join('results', result_filename)
        df.to_csv(result_path, index=False)
        
        # Show results summary
        category_summary = df['predicted_category'].value_counts().to_dict()
        
        return render_template('results.html', 
                             summary=category_summary,
                             filename=result_filename,
                             total=len(df))
    
    return "Invalid file format. Please upload a CSV file.", 400

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join('results', filename), as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)