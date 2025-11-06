# Makefile for AWS Terraform Cost Analyzer

.PHONY: install test clean example help

# Default target
help:
	@echo "AWS Terraform Cost Analyzer"
	@echo "=========================="
	@echo ""
	@echo "Available commands:"
	@echo "  install    - Install dependencies"
	@echo "  test       - Run tests"
	@echo "  example    - Run example analysis"
	@echo "  clean      - Clean up generated files"
	@echo "  lint       - Run code linting"
	@echo "  help       - Show this help message"

# Install dependencies
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed successfully!"

# Run tests
test:
	@echo "Running tests..."
	python test_analyzer.py
	@echo "✅ Tests completed!"

# Run example
example:
	@echo "Running example analysis..."
	@echo "Note: Make sure you have example.tfplan file"
	python example_usage.py

# Clean up
clean:
	@echo "Cleaning up..."
	rm -f *.pyc
	rm -rf __pycache__
	rm -f example_cost_report.txt
	rm -f *.log
	@echo "✅ Cleanup completed!"

# Lint code
lint:
	@echo "Running code linting..."
	python -m py_compile terraform_cost_analyzer.py
	python -m py_compile config.py
	python -m py_compile example_usage.py
	python -m py_compile test_analyzer.py
	@echo "✅ Code linting completed!"

# Quick analysis (requires TFPLAN_FILE environment variable)
analyze:
	@if [ -z "$(TFPLAN_FILE)" ]; then \
		echo "❌ Please set TFPLAN_FILE environment variable"; \
		echo "Example: make analyze TFPLAN_FILE=myplan.tfplan"; \
		exit 1; \
	fi
	@echo "Analyzing $(TFPLAN_FILE)..."
	python terraform_cost_analyzer.py $(TFPLAN_FILE)

# Install as package
install-package:
	@echo "Installing as package..."
	pip install -e .
	@echo "✅ Package installed! You can now use 'terraform-cost-analyzer' command"