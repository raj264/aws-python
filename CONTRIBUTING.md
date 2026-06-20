# Contributing to aws-python

Thank you for your interest in contributing!

## Getting Started

1. Fork the repo and clone it locally
2. Copy `.env.example` to `.env` and fill in your values
3. Install dependencies:
   ```bash
   cd mini_data_pipeline
   pip install -r requirements.txt
   pip install python-dotenv pytest flake8
   ```

## Running Tests

```bash
# mini_data_pipeline
cd mini_data_pipeline && python -m pytest tests/ -v

# unstructured-data-pipeline
cd unstructured-data-pipeline && python -m pytest tests/ -v
```

## Linting

```bash
flake8 mini_data_pipeline --max-line-length=120
flake8 unstructured-data-pipeline --max-line-length=120
```

## Submitting Changes

1. Create a branch: `git checkout -b feature/your-feature-name`
2. Add tests for your changes
3. Ensure tests pass and linting is clean
4. Open a Pull Request with a clear description

## Code Style

- Follow PEP 8, max line length 120
- Add docstrings to all functions
- Never hardcode ARNs or credentials — use environment variables
