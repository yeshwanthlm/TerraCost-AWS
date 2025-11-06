"""
Configuration settings for the Terraform Cost Analyzer
"""

# AWS Bedrock Configuration
BEDROCK_CONFIG = {
    'model_id': 'anthropic.claude-3-sonnet-20240229-v1:0',
    'max_tokens': 4000,
    'temperature': 0.1,
    'top_p': 0.9
}

# Cost Analysis Configuration
COST_CONFIG = {
    'include_hidden_costs': True,
    'include_data_transfer_costs': True,
    'include_recommendations': True,
    'confidence_threshold': 'medium'  # low, medium, high
}

# AWS Resource Types to Analyze
SUPPORTED_RESOURCE_TYPES = [
    'aws_instance',
    'aws_rds_instance',
    'aws_rds_cluster',
    'aws_lambda_function',
    'aws_s3_bucket',
    'aws_ebs_volume',
    'aws_nat_gateway',
    'aws_lb',
    'aws_ecs_service',
    'aws_eks_cluster',
    'aws_cloudfront_distribution',
    'aws_elasticache_cluster',
    'aws_elasticsearch_domain',
    'aws_redshift_cluster',
    'aws_kinesis_stream',
    'aws_api_gateway_rest_api',
    'aws_vpc_endpoint',
    'aws_route53_zone',
    'aws_cloudwatch_log_group'
]

# Default AWS Regions for Cost Analysis
DEFAULT_REGIONS = {
    'us-east-1': 'US East (N. Virginia)',
    'us-west-2': 'US West (Oregon)',
    'eu-west-1': 'Europe (Ireland)',
    'ap-southeast-1': 'Asia Pacific (Singapore)'
}