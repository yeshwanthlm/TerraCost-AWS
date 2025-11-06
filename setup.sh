#!/bin/bash

# AWS Terraform Cost Analyzer Setup Script
# Copyright (c) 2025 Yeshwanth L M
# Licensed under the MIT License. See LICENSE file for details.

set -e

echo "🚀 Setting up AWS Terraform Cost Analyzer..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.8+ required. Found: $python_version"
    exit 1
fi

echo "✅ Python version check passed: $python_version"

# Check if Terraform is installed
if ! command -v terraform &> /dev/null; then
    echo "❌ Terraform CLI not found. Please install Terraform first."
    echo "Visit: https://www.terraform.io/downloads.html"
    exit 1
fi

echo "✅ Terraform CLI found: $(terraform version | head -n1)"

# Check AWS CLI
if ! command -v aws &> /dev/null; then
    echo "⚠️  AWS CLI not found. Please install and configure AWS CLI."
    echo "Visit: https://aws.amazon.com/cli/"
else
    echo "✅ AWS CLI found: $(aws --version)"
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

echo "✅ Dependencies installed successfully!"

# Check AWS credentials
echo "🔐 Checking AWS credentials..."
if aws sts get-caller-identity &> /dev/null; then
    echo "✅ AWS credentials configured"
    aws sts get-caller-identity --query 'Account' --output text | xargs echo "Account ID:"
else
    echo "⚠️  AWS credentials not configured. Please run 'aws configure'"
fi

# Check Bedrock access
echo "🤖 Checking Bedrock access..."
if aws bedrock list-foundation-models --region us-east-1 &> /dev/null; then
    echo "✅ Bedrock access confirmed"
else
    echo "⚠️  Bedrock access not available. Please ensure:"
    echo "   1. Bedrock is enabled in your AWS account"
    echo "   2. You have proper IAM permissions"
    echo "   3. Claude 3 Sonnet model is available in your region"
fi

# Make scripts executable
chmod +x terraform_cost_analyzer.py
chmod +x example_usage.py

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Generate a Terraform plan: terraform plan -out=myplan.tfplan"
echo "2. Run cost analysis: python3 terraform_cost_analyzer.py myplan.tfplan"
echo ""
echo "For help: python3 terraform_cost_analyzer.py --help"