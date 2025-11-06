#!/bin/bash

# AWS Terraform Cost Analyzer - Easy Run Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 AWS Terraform Cost Analyzer${NC}"
echo "=================================="

# Check if tfplan file is provided
if [ $# -eq 0 ]; then
    echo -e "${RED}❌ Error: Please provide a Terraform plan file${NC}"
    echo "Usage: $0 <path-to-tfplan-file> [options]"
    echo ""
    echo "Examples:"
    echo "  $0 terraform/example.tfplan"
    echo "  $0 myplan.tfplan --region us-west-2"
    echo "  $0 myplan.tfplan --output report.txt"
    exit 1
fi

TFPLAN_FILE="$1"
shift # Remove first argument

# Check if tfplan file exists
if [ ! -f "$TFPLAN_FILE" ]; then
    echo -e "${RED}❌ Error: Terraform plan file not found: $TFPLAN_FILE${NC}"
    exit 1
fi

echo -e "${GREEN}📋 Analyzing: $TFPLAN_FILE${NC}"

# Run the cost analyzer
python3 terraform_cost_analyzer.py "$TFPLAN_FILE" "$@"

echo ""
echo -e "${GREEN}✅ Analysis completed!${NC}"