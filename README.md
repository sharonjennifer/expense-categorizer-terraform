# Smart Expense Categorizer - MLOps Project

An ML-powered web application that automatically categorizes expenses using Natural Language Processing. Built with Flask, Scikit-learn, and deployed on Google Cloud Platform using Terraform for Infrastructure as Code.

## Project Overview

This project demonstrates a complete MLOps workflow:
- **ML Model**: Text classification using TF-IDF and Naive Bayes
- **Web Application**: Flask-based interface for CSV upload and categorization
- **Infrastructure as Code**: Terraform for automated GCP resource provisioning
- **Cloud Deployment**: Compute Engine VM with automated startup scripts

## Architecture
```
User → Flask Web App (GCP VM) → ML Model → Categorized Results
                ↓
        GCS Bucket (Storage)
```

**Infrastructure Components:**
- **Compute Engine VM** (e2-medium): Hosts Flask application
- **Cloud Storage Bucket**: Stores data and models
- **Firewall Rules**: Allows HTTP traffic on port 8080
- **Service Account**: Manages GCP permissions

## Dataset

- **Source**: Kaggle Personal Budget Transactions Dataset
- **Records**: 4,597 expense transactions
- **Categories**: 17 categories (Coffee, Market, Restaurant, Transport, etc.)
- **Enhancement**: Added realistic merchant descriptions for ML training

## ML Model

- **Algorithm**: Multinomial Naive Bayes with TF-IDF vectorization
- **Accuracy**: 79.23%
- **Features**: Transaction descriptions (merchant names)
- **Target**: Expense categories

**Model Pipeline:**
```python
TfidfVectorizer → MultinomialNB → Category Prediction
```

## Project Structure
```
expense-categorizer-project/
├── app.py                          # Flask web application
├── train_model.py                  # Model training script
├── enhance_dataset.py              # Dataset enhancement script
├── expense_classifier_model.pkl    # Trained ML model
├── enhanced_expense_data.csv       # Training dataset
├── main.tf                         # Terraform configuration
├── templates/
│   ├── index.html                  # Upload interface
│   └── results.html                # Results display
└── README.md                       # This file
```

## Technologies Used

**Machine Learning:**
- Python 3.13
- Scikit-learn (TF-IDF, Naive Bayes)
- Pandas (Data processing)

**Web Application:**
- Flask (Backend framework)
- HTML/CSS (Frontend)

**Cloud Infrastructure:**
- Google Cloud Platform (GCP)
- Terraform (Infrastructure as Code)
- Compute Engine (VM hosting)
- Cloud Storage (Data storage)

**DevOps:**
- gcloud CLI
- SSH deployment
- Automated startup scripts

## Setup Instructions

### Prerequisites

- GCP account with billing enabled
- Terraform installed
- gcloud CLI configured
- Python 3.9+

### Local Development

1. **Clone and setup:**
```bash
git clone <repository>
cd expense-categorizer-project
pip3 install flask pandas scikit-learn
```

2. **Train the model:**
```bash
python3 enhance_dataset.py
python3 train_model.py
```

3. **Run locally:**
```bash
python3 app.py
# Visit http://localhost:8080
```

### Cloud Deployment with Terraform

1. **Initialize GCP:**
```bash
gcloud init
gcloud auth application-default login
```

2. **Create service account:**
```bash
gcloud iam service-accounts create terraform-sa \
    --display-name="Terraform Service Account"

gcloud projects add-iam-policy-binding terraform-lab-expense \
    --member="serviceAccount:terraform-sa@terraform-lab-expense.iam.gserviceaccount.com" \
    --role="roles/editor"

gcloud iam service-accounts keys create ~/terraform-key.json \
    --iam-account=terraform-sa@terraform-lab-expense.iam.gserviceaccount.com

export GOOGLE_APPLICATION_CREDENTIALS="$HOME/terraform-key.json"
```

3. **Deploy infrastructure:**
```bash
terraform init
terraform plan
terraform apply
```

4. **Deploy application:**
```bash
tar -czf expense-app.tar.gz app.py enhance_dataset.py train_model.py \
  expense_classifier_model.pkl enhanced_expense_data.csv templates/

gcloud compute scp expense-app.tar.gz expense-categorizer-vm:/tmp/ --zone=us-central1-a

gcloud compute ssh expense-categorizer-vm --zone=us-central1-a
cd /opt/expense-app
sudo tar -xzf /tmp/expense-app.tar.gz
sudo python3 app.py
```

5. **Access application:**
```
http://<VM_EXTERNAL_IP>:8080
```

## Usage

1. **Prepare CSV file** with a `description` column:
```csv
description,amount,date
Starbucks Coffee,5.50,2024-01-15
Uber ride,15.00,2024-01-15
Whole Foods Market,45.30,2024-01-16
```

2. **Upload** through web interface

3. **View results** with automatic categorization

4. **Download** categorized CSV file

## Terraform Resources

The `main.tf` file provisions:

- **google_compute_instance**: VM for hosting application
- **google_storage_bucket**: Storage for data/models
- **google_compute_firewall**: HTTP traffic rules
- **random_id**: Unique bucket naming

## Model Performance

**Classification Report:**
```
                   precision    recall  f1-score   support
   Coffee              0.91      1.00      0.95       250
   Market              1.00      0.89      0.94       228
   Restaurant          1.00      1.00      1.00       108
   Transport           1.00      1.00      1.00       104
   ...
```

**Overall Accuracy: 79.23%**

## Cleanup

To destroy all GCP resources:
```bash
terraform destroy
```

Type `yes` when prompted.

## Author

Sharon Jennifer  


