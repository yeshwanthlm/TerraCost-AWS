# Contributing to TerraCost-AWS

Thank you for your interest in contributing to TerraCost-AWS! This document provides guidelines for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Maintain a professional environment

## How to Contribute

### Reporting Issues

1. **Search existing issues** first to avoid duplicates
2. **Use the issue template** when creating new issues
3. **Provide detailed information**:
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, AWS region)
   - Error messages and logs

### Submitting Changes

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**:
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed
4. **Test your changes**:
   - Run existing tests: `python test_analyzer.py`
   - Test with real Terraform plans
   - Verify AWS Bedrock integration
5. **Commit your changes**:
   - Use clear, descriptive commit messages
   - Reference issue numbers when applicable
6. **Push to your fork**: `git push origin feature/your-feature-name`
7. **Create a Pull Request**

### Pull Request Guidelines

- **Clear title and description** explaining the changes
- **Link to related issues** using keywords (fixes #123)
- **Include test results** and example outputs
- **Update documentation** if needed
- **Ensure CI passes** (when implemented)

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/TerraCost-AWS.git
cd TerraCost-AWS

# Install dependencies
pip install -r requirements.txt

# Set up AWS credentials for testing
aws configure

# Run tests
python test_analyzer.py
```

## Code Style Guidelines

### Python Code

- Follow **PEP 8** style guidelines
- Use **type hints** for function parameters and return values
- Add **docstrings** for all functions and classes
- Use **meaningful variable names**
- Keep functions **focused and small**

### Documentation

- Update **README.md** for user-facing changes
- Update **USAGE_GUIDE.md** for new features
- Add **inline comments** for complex logic
- Include **examples** for new functionality

### Testing

- Add **unit tests** for new functions
- Include **integration tests** for AWS services
- Test with **multiple Terraform configurations**
- Verify **error handling** scenarios

## Areas for Contribution

### High Priority

- **Additional AWS Resources**: Support for more AWS services
- **Cost Optimization**: Enhanced recommendations engine
- **Performance**: Faster analysis for large Terraform plans
- **Error Handling**: Better error messages and recovery

### Medium Priority

- **Multi-Region Analysis**: Compare costs across regions
- **Historical Tracking**: Cost trend analysis
- **CI/CD Integration**: GitHub Actions, GitLab CI support
- **Output Formats**: JSON, CSV, HTML reports

### Low Priority

- **GUI Interface**: Web-based dashboard
- **Terraform Cloud Integration**: Direct API integration
- **Cost Alerts**: Threshold-based notifications
- **Multi-Cloud Support**: Azure, GCP cost analysis

## AWS Bedrock Considerations

When working with Bedrock integration:

- **Test with different models** (Claude, Titan, etc.)
- **Handle rate limits** gracefully
- **Validate JSON responses** thoroughly
- **Consider cost implications** of API calls
- **Test in multiple AWS regions**

## Security Guidelines

- **Never commit credentials** or sensitive data
- **Use IAM roles** instead of access keys when possible
- **Validate all inputs** to prevent injection attacks
- **Follow AWS security best practices**
- **Report security issues** privately

## Documentation Standards

- Use **clear, concise language**
- Include **code examples** for new features
- Add **screenshots** for UI changes
- Update **API documentation** for new functions
- Maintain **changelog** for releases

## Release Process

1. **Update version** in setup.py
2. **Update CHANGELOG.md** with new features and fixes
3. **Create release notes** with examples
4. **Tag the release**: `git tag v1.x.x`
5. **Push tags**: `git push --tags`

## Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Email**: For security issues or private matters

## License

By contributing to TerraCost-AWS, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in:
- **README.md** contributors section
- **Release notes** for significant contributions
- **GitHub contributors** page

Thank you for helping make TerraCost-AWS better! 🚀