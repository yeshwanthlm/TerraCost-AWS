#!/usr/bin/env python3
"""
AWS Terraform Cost Analyzer
A tool to analyze Terraform plans and estimate AWS costs using Bedrock AI
"""

import json
import subprocess
import sys
import os
from typing import Dict, List, Any, Optional
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
import argparse
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TerraformCostAnalyzer:
    def __init__(self, aws_region: str = 'us-east-1'):
        """Initialize the cost analyzer with AWS clients"""
        self.aws_region = aws_region
        self.bedrock_client = None
        self.pricing_client = None
        self._initialize_aws_clients()
        
    def _initialize_aws_clients(self):
        """Initialize AWS clients with error handling"""
        try:
            # Initialize Bedrock client
            self.bedrock_client = boto3.client(
                'bedrock-runtime',
                region_name=self.aws_region
            )
            
            # Initialize Pricing client (always use us-east-1 for pricing)
            self.pricing_client = boto3.client(
                'pricing',
                region_name='us-east-1'
            )
            
            logger.info("AWS clients initialized successfully")
            
        except NoCredentialsError:
            logger.error("AWS credentials not found. Please configure your credentials.")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Failed to initialize AWS clients: {str(e)}")
            sys.exit(1)
            
    def parse_terraform_plan(self, tfplan_file: str) -> Dict[str, Any]:
        """Parse Terraform plan file and extract resource information"""
        try:
            # Get the directory containing the tfplan file
            plan_dir = os.path.dirname(os.path.abspath(tfplan_file))
            plan_filename = os.path.basename(tfplan_file)
            
            # Convert binary tfplan to JSON
            result = subprocess.run(
                ['terraform', 'show', '-json', plan_filename],
                capture_output=True,
                text=True,
                check=True,
                cwd=plan_dir  # Run from the plan directory
            )
            
            plan_data = json.loads(result.stdout)
            logger.info(f"Successfully parsed Terraform plan: {tfplan_file}")
            
            return self._extract_resources(plan_data)
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to parse Terraform plan: {e.stderr}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON output: {str(e)}")
            raise
        except FileNotFoundError:
            logger.error("Terraform CLI not found. Please install Terraform.")
            raise

    def _extract_resources(self, plan_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract relevant resource information from plan data"""
        resources = {
            'create': [],
            'update': [],
            'delete': []
        }
        
        if 'resource_changes' not in plan_data:
            logger.warning("No resource changes found in plan")
            return resources
            
        for change in plan_data['resource_changes']:
            action = change.get('change', {}).get('actions', [])
            
            if 'create' in action:
                resources['create'].append(self._format_resource(change))
            elif 'update' in action:
                resources['update'].append(self._format_resource(change))
            elif 'delete' in action:
                resources['delete'].append(self._format_resource(change))
                
        return resources

    def _format_resource(self, change: Dict[str, Any]) -> Dict[str, Any]:
        """Format resource information for cost analysis"""
        return {
            'type': change.get('type', ''),
            'name': change.get('name', ''),
            'address': change.get('address', ''),
            'values': change.get('change', {}).get('after', {}),
            'provider': change.get('provider_name', 'aws')
        }

    def analyze_costs_with_bedrock(self, resources: Dict[str, Any]) -> Dict[str, Any]:
        """Use Bedrock to analyze costs for AWS resources"""
        cost_analysis = {
            'total_estimated_cost': 0.0,
            'monthly_cost_breakdown': {},
            'hidden_costs': [],
            'data_transfer_costs': [],
            'recommendations': []
        }
        
        for action, resource_list in resources.items():
            if action == 'delete':
                continue  # Skip deleted resources for cost calculation
                
            for resource in resource_list:
                try:
                    resource_cost = self._get_resource_cost_estimate(resource)
                    if resource_cost:
                        cost_analysis['monthly_cost_breakdown'][resource['address']] = resource_cost
                        cost_analysis['total_estimated_cost'] += resource_cost.get('monthly_cost', 0)
                        
                        # Add hidden costs if any
                        if resource_cost.get('hidden_costs'):
                            cost_analysis['hidden_costs'].extend(resource_cost['hidden_costs'])
                            
                        # Add data transfer costs if any
                        if resource_cost.get('data_transfer_costs'):
                            cost_analysis['data_transfer_costs'].extend(resource_cost['data_transfer_costs'])
                            
                except Exception as e:
                    logger.warning(f"Failed to analyze cost for {resource['address']}: {str(e)}")
                    
        return cost_analysis

    def _get_resource_cost_estimate(self, resource: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get cost estimate for a specific resource using Bedrock"""
        resource_type = resource['type']
        resource_config = resource['values']
        
        # Create a detailed prompt for Bedrock
        prompt = self._create_cost_analysis_prompt(resource_type, resource_config)
        
        try:
            response = self._call_bedrock(prompt)
            return self._parse_bedrock_response(response, resource)
            
        except Exception as e:
            logger.error(f"Bedrock analysis failed for {resource['address']}: {str(e)}")
            return None

    def _create_cost_analysis_prompt(self, resource_type: str, config: Dict[str, Any]) -> str:
        """Create a detailed prompt for Bedrock cost analysis"""
        prompt = f"""
You are an AWS cost analysis expert. Analyze the following AWS resource and provide detailed cost estimates.

Resource Type: {resource_type}
Configuration: {json.dumps(config, indent=2)}
Region: {self.aws_region}
Analysis Date: {datetime.now().strftime('%Y-%m-%d')}

Please provide a comprehensive cost analysis including:

1. MONTHLY COST ESTIMATE:
   - Base monthly cost for the resource
   - Include all pricing tiers and usage patterns
   - Consider reserved instance discounts if applicable

2. HIDDEN COSTS:
   - Data transfer costs (inbound/outbound)
   - Storage costs (if applicable)
   - Network costs (NAT Gateway, Load Balancer data processing)
   - Backup and snapshot costs
   - Monitoring and logging costs

3. VARIABLE COSTS:
   - Usage-based pricing components
   - Potential cost spikes during high usage
   - Scaling cost implications

4. COST OPTIMIZATION RECOMMENDATIONS:
   - Suggest cost-effective alternatives
   - Reserved instance opportunities
   - Right-sizing recommendations

Respond in JSON format:
{{
  "monthly_cost": <number>,
  "cost_breakdown": {{
    "compute": <number>,
    "storage": <number>,
    "network": <number>,
    "other": <number>
  }},
  "hidden_costs": [
    {{
      "type": "<cost_type>",
      "description": "<description>",
      "estimated_monthly_cost": <number>
    }}
  ],
  "data_transfer_costs": [
    {{
      "type": "<transfer_type>",
      "description": "<description>",
      "estimated_monthly_cost": <number>
    }}
  ],
  "recommendations": [
    "<recommendation_text>"
  ],
  "confidence_level": "<high|medium|low>"
}}
"""
        return prompt

    def _call_bedrock(self, prompt: str) -> str:
        """Call Bedrock API for cost analysis"""
        try:
            # Using Claude 3 Sonnet for cost analysis
            model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
            
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4000,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.1,
                "top_p": 0.9
            }
            
            response = self.bedrock_client.invoke_model(
                modelId=model_id,
                body=json.dumps(body)
            )
            
            response_body = json.loads(response['body'].read())
            return response_body['content'][0]['text']
            
        except ClientError as e:
            logger.error(f"Bedrock API error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error calling Bedrock: {str(e)}")
            raise

    def _parse_bedrock_response(self, response: str, resource: Dict[str, Any]) -> Dict[str, Any]:
        """Parse Bedrock response and extract cost information"""
        try:
            # Extract JSON from response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                logger.warning(f"No JSON found in Bedrock response for {resource['address']}")
                return None
                
            json_str = response[start_idx:end_idx]
            cost_data = json.loads(json_str)
            
            # Validate required fields
            required_fields = ['monthly_cost', 'cost_breakdown']
            for field in required_fields:
                if field not in cost_data:
                    logger.warning(f"Missing required field '{field}' in cost analysis")
                    return None
                    
            return cost_data
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Bedrock JSON response: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error parsing Bedrock response: {str(e)}")
            return None

    def generate_cost_report(self, cost_analysis: Dict[str, Any], output_file: str = None) -> str:
        """Generate a comprehensive cost report"""
        report = []
        report.append("=" * 80)
        report.append("AWS TERRAFORM COST ANALYSIS REPORT")
        report.append("=" * 80)
        report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Region: {self.aws_region}")
        report.append("")
        
        # Summary
        report.append("COST SUMMARY")
        report.append("-" * 40)
        report.append(f"Total Estimated Monthly Cost: ${cost_analysis['total_estimated_cost']:.2f}")
        report.append("")
        
        # Resource breakdown
        if cost_analysis['monthly_cost_breakdown']:
            report.append("RESOURCE COST BREAKDOWN")
            report.append("-" * 40)
            for resource, cost_info in cost_analysis['monthly_cost_breakdown'].items():
                monthly_cost = cost_info.get('monthly_cost', 0)
                report.append(f"{resource}: ${monthly_cost:.2f}/month")
                
                # Show cost breakdown if available
                if 'cost_breakdown' in cost_info:
                    breakdown = cost_info['cost_breakdown']
                    for category, amount in breakdown.items():
                        if amount > 0:
                            report.append(f"  - {category.title()}: ${amount:.2f}")
            report.append("")
        
        # Hidden costs
        if cost_analysis['hidden_costs']:
            report.append("HIDDEN COSTS")
            report.append("-" * 40)
            total_hidden = 0
            for cost in cost_analysis['hidden_costs']:
                amount = cost.get('estimated_monthly_cost', 0)
                total_hidden += amount
                report.append(f"• {cost['type']}: ${amount:.2f}/month")
                report.append(f"  {cost['description']}")
            report.append(f"Total Hidden Costs: ${total_hidden:.2f}/month")
            report.append("")
        
        # Data transfer costs
        if cost_analysis['data_transfer_costs']:
            report.append("DATA TRANSFER COSTS")
            report.append("-" * 40)
            total_transfer = 0
            for cost in cost_analysis['data_transfer_costs']:
                amount = cost.get('estimated_monthly_cost', 0)
                total_transfer += amount
                report.append(f"• {cost['type']}: ${amount:.2f}/month")
                report.append(f"  {cost['description']}")
            report.append(f"Total Data Transfer Costs: ${total_transfer:.2f}/month")
            report.append("")
        
        # Recommendations
        if cost_analysis['recommendations']:
            report.append("COST OPTIMIZATION RECOMMENDATIONS")
            report.append("-" * 40)
            for i, recommendation in enumerate(cost_analysis['recommendations'], 1):
                report.append(f"{i}. {recommendation}")
            report.append("")
        
        report_text = "\n".join(report)
        
        # Save to file if specified
        if output_file:
            try:
                with open(output_file, 'w') as f:
                    f.write(report_text)
                logger.info(f"Cost report saved to: {output_file}")
            except Exception as e:
                logger.error(f"Failed to save report to file: {str(e)}")
        
        return report_text

def main():
    """Main function to run the cost analyzer"""
    parser = argparse.ArgumentParser(
        description="Analyze AWS costs for Terraform plans using Bedrock AI"
    )
    parser.add_argument(
        'tfplan_file',
        help='Path to the Terraform plan file (.tfplan)'
    )
    parser.add_argument(
        '--region',
        default='us-east-1',
        help='AWS region for cost analysis (default: us-east-1)'
    )
    parser.add_argument(
        '--output',
        help='Output file for the cost report'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Validate input file
    if not os.path.exists(args.tfplan_file):
        logger.error(f"Terraform plan file not found: {args.tfplan_file}")
        sys.exit(1)
    
    try:
        # Initialize analyzer
        logger.info("Initializing AWS Terraform Cost Analyzer...")
        analyzer = TerraformCostAnalyzer(aws_region=args.region)
        
        # Parse Terraform plan
        logger.info("Parsing Terraform plan...")
        resources = analyzer.parse_terraform_plan(args.tfplan_file)
        
        if not any(resources.values()):
            logger.warning("No resources found in Terraform plan")
            return
        
        logger.info(f"Found {sum(len(v) for v in resources.values())} resources to analyze")
        
        # Analyze costs
        logger.info("Analyzing costs with Bedrock AI...")
        cost_analysis = analyzer.analyze_costs_with_bedrock(resources)
        
        # Generate report
        logger.info("Generating cost report...")
        report = analyzer.generate_cost_report(cost_analysis, args.output)
        
        # Print report to console
        print(report)
        
        logger.info("Cost analysis completed successfully!")
        
    except KeyboardInterrupt:
        logger.info("Analysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()