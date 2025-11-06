#!/usr/bin/env python3
"""
Test script for the Terraform Cost Analyzer

Copyright (c) 2025 Yeshwanth L M
Licensed under the MIT License. See LICENSE file for details.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import json
from terraform_cost_analyzer import TerraformCostAnalyzer

class TestTerraformCostAnalyzer(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        with patch('boto3.client'):
            self.analyzer = TerraformCostAnalyzer()
    
    def test_format_resource(self):
        """Test resource formatting"""
        change = {
            'type': 'aws_instance',
            'name': 'web_server',
            'address': 'aws_instance.web_server',
            'change': {
                'after': {
                    'instance_type': 't3.medium',
                    'ami': 'ami-12345'
                }
            },
            'provider_name': 'aws'
        }
        
        result = self.analyzer._format_resource(change)
        
        self.assertEqual(result['type'], 'aws_instance')
        self.assertEqual(result['name'], 'web_server')
        self.assertEqual(result['address'], 'aws_instance.web_server')
        self.assertEqual(result['values']['instance_type'], 't3.medium')
    
    def test_create_cost_analysis_prompt(self):
        """Test prompt creation"""
        resource_type = 'aws_instance'
        config = {'instance_type': 't3.medium', 'ami': 'ami-12345'}
        
        prompt = self.analyzer._create_cost_analysis_prompt(resource_type, config)
        
        self.assertIn('aws_instance', prompt)
        self.assertIn('t3.medium', prompt)
        self.assertIn('MONTHLY COST ESTIMATE', prompt)
        self.assertIn('HIDDEN COSTS', prompt)
    
    def test_parse_bedrock_response(self):
        """Test Bedrock response parsing"""
        response = '''
        Here's the cost analysis:
        {
          "monthly_cost": 65.50,
          "cost_breakdown": {
            "compute": 58.00,
            "storage": 7.50
          },
          "hidden_costs": [],
          "recommendations": ["Use Reserved Instances"]
        }
        '''
        
        resource = {'address': 'aws_instance.test'}
        result = self.analyzer._parse_bedrock_response(response, resource)
        
        self.assertEqual(result['monthly_cost'], 65.50)
        self.assertEqual(result['cost_breakdown']['compute'], 58.00)
    
    @patch('subprocess.run')
    def test_parse_terraform_plan(self, mock_run):
        """Test Terraform plan parsing"""
        mock_output = {
            'resource_changes': [
                {
                    'type': 'aws_instance',
                    'name': 'web',
                    'address': 'aws_instance.web',
                    'change': {
                        'actions': ['create'],
                        'after': {'instance_type': 't3.micro'}
                    }
                }
            ]
        }
        
        mock_run.return_value.stdout = json.dumps(mock_output)
        mock_run.return_value.returncode = 0
        
        result = self.analyzer.parse_terraform_plan('test.tfplan')
        
        self.assertEqual(len(result['create']), 1)
        self.assertEqual(result['create'][0]['type'], 'aws_instance')

def run_tests():
    """Run all tests"""
    unittest.main(verbosity=2)

if __name__ == '__main__':
    run_tests()