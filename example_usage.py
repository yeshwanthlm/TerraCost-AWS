#!/usr/bin/env python3
"""
Example usage of the Terraform Cost Analyzer

Copyright (c) 2025 Yeshwanth L M
Licensed under the MIT License. See LICENSE file for details.
"""

import os
import sys
from terraform_cost_analyzer import TerraformCostAnalyzer

def run_example():
    """Run an example cost analysis"""
    
    # Check if example tfplan file exists
    example_plan = "example.tfplan"
    
    if not os.path.exists(example_plan):
        print("Example tfplan file not found. Please create one with:")
        print("terraform plan -out=example.tfplan")
        return
    
    try:
        # Initialize analyzer
        print("🚀 Initializing AWS Terraform Cost Analyzer...")
        analyzer = TerraformCostAnalyzer(aws_region='us-east-1')
        
        # Parse plan
        print("📋 Parsing Terraform plan...")
        resources = analyzer.parse_terraform_plan(example_plan)
        
        print(f"Found resources:")
        for action, resource_list in resources.items():
            if resource_list:
                print(f"  {action}: {len(resource_list)} resources")
        
        # Analyze costs
        print("💰 Analyzing costs with Bedrock AI...")
        cost_analysis = analyzer.analyze_costs_with_bedrock(resources)
        
        # Generate report
        print("📊 Generating cost report...")
        report = analyzer.generate_cost_report(cost_analysis, "example_cost_report.txt")
        
        print("\n" + "="*60)
        print("COST ANALYSIS COMPLETE!")
        print("="*60)
        print(f"Total Monthly Cost: ${cost_analysis['total_estimated_cost']:.2f}")
        print("Full report saved to: example_cost_report.txt")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_example()