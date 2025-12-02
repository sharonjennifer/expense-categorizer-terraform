# Configure the Google Cloud provider
provider "google" {
  project = "terraform-lab-expense"
  region  = "us-central1"
  zone    = "us-central1-a"
}

# Create a GCS bucket for storing data and models
resource "google_storage_bucket" "expense_bucket" {
  name          = "expense-categorizer-bucket-${random_id.bucket_suffix.hex}"
  location      = "US"
  force_destroy = true

  uniform_bucket_level_access = true
}

# Generate random suffix for bucket name (must be globally unique)
resource "random_id" "bucket_suffix" {
  byte_length = 4
}

# Create a Compute Engine VM instance
resource "google_compute_instance" "expense_vm" {
  name         = "expense-categorizer-vm"
  machine_type = "e2-medium"
  zone         = "us-central1-a"

  tags = ["http-server", "https-server"]

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
      size  = 20
    }
  }

  network_interface {
    network = "default"
    access_config {
      # Ephemeral public IP
    }
  }

  # Startup script to install dependencies and run the Flask app
  metadata_startup_script = <<-EOF
    #!/bin/bash
    apt-get update
    apt-get install -y python3-pip git
    
    # Create app directory
    mkdir -p /opt/expense-app
    cd /opt/expense-app
    
    # Install Python packages
    pip3 install flask pandas scikit-learn
    
    # Create a placeholder message
    cat > /opt/expense-app/startup_complete.txt << 'INNER_EOF'
    VM is ready! 
    Next: Upload your application files via SCP or Cloud Console.
    INNER_EOF
    
    echo "Startup script completed" > /var/log/startup-complete.log
  EOF

  service_account {
    email  = "terraform-sa@terraform-lab-expense.iam.gserviceaccount.com"
    scopes = ["cloud-platform"]
  }
}

# Firewall rule to allow HTTP traffic
resource "google_compute_firewall" "allow_http" {
  name    = "allow-http-expense-app"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["8080"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["http-server"]
}

# Output the VM's external IP address
output "vm_external_ip" {
  value       = google_compute_instance.expense_vm.network_interface[0].access_config[0].nat_ip
  description = "External IP address of the VM"
}

# Output the bucket name
output "bucket_name" {
  value       = google_storage_bucket.expense_bucket.name
  description = "Name of the GCS bucket"
}