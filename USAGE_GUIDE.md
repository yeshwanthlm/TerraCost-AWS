# AWS Terraform Cost Analyzer - Usage Guide

## Quick Start

### 1. Setup
```bash
# Run the setup script
./setup.sh

# Or manual setup
pip install -r requirements.txt
```

### 2. Generate Terraform Plan
```bash
# Initialize Terraform (if not done already)
terraform init

# Create a plan file
terraform plan -out=myplan.tfplan
```

### 3. Analyze Costs
```bash
# Basic analysis
python terraform_cost_analyzer.py myplan.tfplan

# With custom region and output file
python terraform_cost_analyzer.py myplan.tfplan --region us-west-2 --output report.txt

# Verbose mode for debugging
python terraform_cost_analyzer.py myplan.tfplan --verbose
```

## Example Workflow

### Step 1: Create Example Infrastructure
```bash
# Use the provided example
terraform init
terraform plan -out=example.tfplan -var-file=example.tf
```

### Step 2: Run Cost Analysis
```bash
python terraform_cost_analyzer.py example.tfplan --output example_report.txt
```

### Step 3: Review Results
The tool will output:
- Total monthly cost estimate
- Per-resource cost breakdown
- Hidden costs (data transfer, NAT processing, etc.)
- Cost optimization recommendations

## Advanced Usage

### Custom Configuration
Edit `config.py` to customize:
- Bedrock model settings
- Supported resource types
- Analysis parameters

### Batch Analysis
```bash
# Analyze multiple plans
for plan in *.tfplan; do
    python terraform_cost_analyzer.py "$plan" --output "${plan%.tfplan}_report.txt"
done
```

### Integration with CI/CD
```yaml
# GitHub Actions example
- name: Terraform Cost Analysis
  run: |
    terraform plan -out=plan.tfplan
    python terraform_cost_analyzer.py plan.tfplan --output cost_report.txt
    cat cost_report.txt >> $GITHUB_STEP_SUMMARY
```

## Troubleshooting

### Common Issues

1. **"Bedrock Access Denied"**
   - Ensure Bedrock is enabled in your AWS account
   - Check IAM permissions for `bedrock:InvokeModel`
   - Verify Claude 3 Sonnet access in your region

2. **"Terraform Command Not Found"**
   - Install Terraform CLI from https://terraform.io
   - Ensure it's in your system PATH

3. **"AWS Credentials Not Found"**
   - Run `aws configure` to set up credentials
   - Or use IAM roles/environment variables

4. **"No Resources Found"**
   - Ensure your Terraform plan has resource changes
   - Check that the plan file is not empty: `terraform show plan.tfplan`

### Debug Mode
```bash
python terraform_cost_analyzer.py myplan.tfplan --verbose
```

### Test Installation
```bash
# Run tests
python test_analyzer.py

# Or use make
make test
```

## Cost Estimation Accuracy

The tool provides estimates based on:
- Current AWS pricing (via Bedrock AI)
- Resource configurations in your Terraform plan
- Regional pricing differences
- Usage patterns and assumptions

**Note**: Actual costs may vary based on:
- Real usage patterns
- Reserved instance discounts
- Volume discounts
- Promotional credits

## Security Best Practices

1. **Use IAM Roles**: Prefer IAM roles over access keys
2. **Least Privilege**: Grant minimal required permissions
3. **Audit Logs**: Monitor Bedrock API usage
4. **Secure Plans**: Don't commit `.tfplan` files to version control

## Performance Tips

1. **Regional Analysis**: Use the same region as your resources
2. **Batch Processing**: Analyze multiple resources together
3. **Caching**: Results are not cached - re-run for updated pricing
4. **Parallel Processing**: The tool processes resources in parallel

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review AWS Bedrock documentation
3. Verify Terraform plan format
4. Check AWS service limits and quotas