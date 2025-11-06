# AWS Terraform Cost Analyzer

An intelligent cost estimation tool that analyzes Terraform plans and provides detailed AWS cost breakdowns using Amazon Bedrock AI.

## Features

- **AI-Powered Analysis**: Uses Amazon Bedrock (Claude 3 Sonnet) for intelligent cost estimation
- **Comprehensive Cost Breakdown**: Analyzes base costs, hidden costs, and data transfer costs
- **Real-time Pricing**: Gets current AWS pricing without hardcoded values
- **Hidden Cost Detection**: Identifies often-overlooked costs like data transfer, NAT Gateway processing, etc.
- **Cost Optimization**: Provides recommendations for cost reduction
- **Secure**: Uses AWS IAM for authentication, no hardcoded credentials
- **Fast**: Parallel processing and efficient API calls

## Prerequisites

1. **AWS CLI configured** with appropriate credentials
2. **Terraform CLI** installed and accessible
3. **AWS Bedrock access** enabled in your AWS account
4. **Python 3.8+**

## Installation

```bash
# Clone or download the tool
pip install -r requirements.txt

# Or install as a package
pip install -e .
```

## AWS Setup

1. **Enable Bedrock Access**:
   ```bash
   # Ensure you have access to Claude 3 Sonnet in your AWS region
   aws bedrock list-foundation-models --region us-east-1
   ```

2. **Required IAM Permissions**:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "bedrock:InvokeModel",
           "pricing:GetProducts",
           "pricing:DescribeServices"
         ],
         "Resource": "*"
       }
     ]
   }
   ```

## Usage

### Basic Usage

```bash
# Generate Terraform plan
terraform plan -out=myplan.tfplan

# Analyze costs
python terraform_cost_analyzer.py myplan.tfplan
```

### Advanced Usage

```bash
# Specify region and output file
python terraform_cost_analyzer.py myplan.tfplan --region us-west-2 --output cost_report.txt

# Enable verbose logging
python terraform_cost_analyzer.py myplan.tfplan --verbose
```

### Example Output

```
================================================================================
AWS TERRAFORM COST ANALYSIS REPORT
================================================================================
Generated on: 2024-11-06 10:30:45
Region: us-east-1

COST SUMMARY
----------------------------------------
Total Estimated Monthly Cost: $245.67

RESOURCE COST BREAKDOWN
----------------------------------------
aws_instance.web_server: $72.00/month
  - Compute: $65.00
  - Storage: $7.00
aws_rds_instance.database: $156.50/month
  - Compute: $140.00
  - Storage: $16.50

HIDDEN COSTS
----------------------------------------
• Data Transfer: $12.50/month
  Outbound data transfer from EC2 to internet
• NAT Gateway Processing: $4.67/month
  Data processing charges for NAT Gateway

COST OPTIMIZATION RECOMMENDATIONS
----------------------------------------
1. Consider using Reserved Instances for 40% savings on EC2
2. Enable GP3 storage for better price/performance ratio
3. Use CloudFront to reduce data transfer costs
```

## Configuration

Edit `config.py` to customize:

- Bedrock model settings
- Supported resource types
- Analysis parameters
- Default regions

## Security Features

- **No Hardcoded Credentials**: Uses AWS IAM roles and profiles
- **Least Privilege**: Only requires read-only pricing and Bedrock access
- **Input Validation**: Validates Terraform plan files before processing
- **Error Handling**: Comprehensive error handling and logging

## Supported AWS Resources

- EC2 Instances
- RDS Instances and Clusters
- Lambda Functions
- S3 Buckets
- EBS Volumes
- NAT Gateways
- Load Balancers
- ECS Services
- EKS Clusters
- CloudFront Distributions
- ElastiCache Clusters
- And many more...

## Troubleshooting

### Common Issues

1. **Bedrock Access Denied**:
   - Ensure Bedrock is enabled in your region
   - Check IAM permissions
   - Verify model access

2. **Terraform Command Not Found**:
   - Install Terraform CLI
   - Ensure it's in your PATH

3. **AWS Credentials Not Found**:
   - Configure AWS CLI: `aws configure`
   - Or use IAM roles/environment variables

### Debug Mode

```bash
python terraform_cost_analyzer.py myplan.tfplan --verbose
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details.