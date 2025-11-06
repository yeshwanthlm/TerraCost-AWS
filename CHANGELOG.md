# Changelog

All notable changes to TerraCost-AWS will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-06

### Added
- Initial release of TerraCost-AWS
- AI-powered cost analysis using Amazon Bedrock (Claude 3 Sonnet)
- Support for major AWS resources (EC2, RDS, Lambda, S3, etc.)
- Hidden cost detection (data transfer, NAT Gateway processing, etc.)
- Real-time pricing without hardcoded values
- Comprehensive cost breakdown and reporting
- Cost optimization recommendations
- Security group analysis
- Command-line interface with multiple options
- Automated setup script (`setup.sh`)
- Convenience wrapper script (`analyze_costs.sh`)
- Example Terraform configuration
- Comprehensive documentation and usage guide
- Unit tests and example usage scripts
- MIT License
- Contributing guidelines

### Features
- **Core Analysis Engine**: Parse Terraform plans and extract resource information
- **Bedrock Integration**: Use AI for intelligent cost estimation
- **Cost Breakdown**: Detailed monthly cost analysis per resource
- **Hidden Costs**: Identify often-overlooked costs like data transfer
- **Optimization**: AI-powered cost reduction recommendations
- **Security**: IAM-based authentication, no hardcoded credentials
- **Performance**: Parallel processing for multiple resources
- **Flexibility**: Configurable regions, output formats, and verbosity
- **Documentation**: Complete setup and usage documentation

### Supported AWS Resources
- EC2 Instances
- RDS Instances and Clusters
- Lambda Functions
- S3 Buckets
- EBS Volumes
- NAT Gateways
- Load Balancers (ALB/NLB)
- Security Groups
- ECS Services
- EKS Clusters
- CloudFront Distributions
- ElastiCache Clusters
- And more...

### Technical Details
- **Language**: Python 3.8+
- **Dependencies**: boto3, botocore
- **AI Model**: Anthropic Claude 3 Sonnet via Amazon Bedrock
- **Authentication**: AWS IAM roles and profiles
- **Output**: Text reports with optional file output
- **Error Handling**: Comprehensive logging and error recovery

### Usage
```bash
# Basic usage
python terraform_cost_analyzer.py myplan.tfplan

# Advanced usage
python terraform_cost_analyzer.py myplan.tfplan --region us-west-2 --output report.txt --verbose
```

### Installation
```bash
git clone https://github.com/yeshwanthlm/TerraCost-AWS.git
cd TerraCost-AWS
./setup.sh
```

## [Unreleased]

### Planned Features
- Multi-region cost comparison
- Historical cost tracking
- Additional output formats (JSON, CSV, HTML)
- CI/CD integration templates
- Enhanced error handling and recovery
- Support for more AWS services
- Performance optimizations for large plans

---

## Version History

- **v1.0.0** - Initial release with core functionality
- **Future versions** - See GitHub releases for detailed changelogs