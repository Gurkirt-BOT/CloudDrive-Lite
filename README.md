# CloudDrive Lite

CloudDrive Lite is a simple cloud-based file storage web application built using:

- Streamlit (Frontend)
- EC2 (Compute)
- S3 (Storage)
- IAM Role (Secure Access)
- VPC (Networking)

## Features

- User enters username
- Upload files
- View uploaded files
- Files stored securely in S3
- No hardcoded AWS credentials

## Architecture

User → EC2 (Streamlit App) → S3 Bucket

## How to Run

1. Launch EC2 instance
2. Attach IAM Role with S3 access
3. Install dependencies:
   pip3 install -r requirements.txt
4. Run:
   streamlit run app.py --server.port 8501 --server.address 0.0.0.0
