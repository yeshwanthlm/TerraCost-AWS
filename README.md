# TerraCost-AWS

An intelligent AWS cost estimation tool that analyzes Terraform plans and provides detailed cost breakdowns using Amazon Bedrock AI.

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
# Clone the repository
git clone https://github.com/yeshwanthlm/TerraCost-AWS.git
cd TerraCost-AWS

# Run setup script
./setup.sh

# Or manual installation
pip install -r requirements.txt
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

# Or use the convenience script
./analyze_costs.sh myplan.tfplan
```

### Advanced Usage

```bash
# Specify region and output file
python terraform_cost_analyzer.py myplan.tfplan --region us-west-2 --output cost_report.txt

# Enable verbose logging
python terraform_cost_analyzer.py myplan.tfplan --verbose
```

### Example with Provided Configuration

```bash
# Use the example Terraform configuration
cd terraform
terraform init
terraform plan -out=example.tfplan

# Analyze the example
cd ..
./analyze_costs.sh terraform/example.tfplan
```

### Example Output

```
================================================================================
AWS TERRAFORM COST ANALYSIS REPORT
================================================================================
Generated on: 2025-11-06 12:06:22
Region: us-east-1

COST SUMMARY
----------------------------------------
Total Estimated Monthly Cost: $8.47

RESOURCE COST BREAKDOWN
----------------------------------------
aws_instance.ubuntu_server: $8.47/month
  - Compute: $8.47
aws_security_group.allow_all: $0.00/month

HIDDEN COSTS
----------------------------------------
• Data Transfer: $0.00/month
  Inbound data transfer is free, but outbound data transfer is charged based on usage
• Monitoring and Logging: $0.00/month
  AWS CloudWatch monitoring and logging charges apply based on usage
Total Hidden Costs: $0.00/month
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
- Security Groups
- And many more...

## Project Structure

```
TerraCost-AWS/
├── terraform_cost_analyzer.py    # Main analyzer tool
├── config.py                     # Configuration settings
├── requirements.txt              # Python dependencies
├── setup.sh                      # Setup script
├── analyze_costs.sh              # Convenience script
├── Makefile                      # Build commands
├── terraform/
│   └── example.tf               # Example Terraform config
├── test_analyzer.py             # Unit tests
├── example_usage.py             # Usage examples
├── USAGE_GUIDE.md              # Detailed usage guide
└── README.md                   # This file
```

## 💰 Tool Usage Costs

**Primary Cost: Amazon Bedrock API calls (Claude 3 Sonnet)**

### Realistic Cost Calculation
**Bedrock Pricing (Claude 3 Sonnet):**
- Input tokens: $0.003 per 1,000 tokens
- Output tokens: $0.015 per 1,000 tokens

**Actual Token Usage per Resource:**
- Input: ~500-800 tokens (prompt + resource config)
- Output: ~300-500 tokens (cost analysis response)
- **Cost per resource: ~$0.003-0.005** (0.3-0.5 cents)

### Per Analysis Cost
- **Small plan (3 resources)**: ~$0.01-0.02
- **Medium plan (15 resources)**: ~$0.05-0.08  
- **Large plan (50 resources)**: ~$0.15-0.25

### Cost for 10,000 Analyses
- **Small plans**: $100-200
- **Medium plans**: $500-800
- **Large plans**: $1,500-2,500

### Where Costs Come From
1. **Bedrock API calls** - Only cost component
2. **AWS Pricing API** - FREE
3. **Data transfer** - Negligible

### ROI Example
Even at higher usage (large plans), monthly cost is typically $50-150, while potential AWS savings from optimization can be $1,000+ per month.

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
