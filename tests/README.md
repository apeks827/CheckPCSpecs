# Test Suite Documentation

## Overview

This test suite provides comprehensive coverage for the CheckPCSpecs application, including unit tests, integration tests, and fixtures.

## Structure

```
tests/
├── __init__.py              # Test package marker
├── conftest.py              # Pytest configuration and shared fixtures
├── README.md                # This file
├── unit/                    # Unit tests
│   ├── __init__.py
│   ├── test_models.py       # Tests for data models
│   ├── test_specs_checker.py # Tests for specs evaluation logic
│   ├── test_network.py      # Tests for network testing modules
│   └── test_utils.py        # Tests for utility functions
└── integration/             # Integration tests
    ├── __init__.py
    └── test_full_check.py   # End-to-end system check tests
```

## Running Tests

### Install Development Dependencies

```bash
pip install -e ".[dev]"
```

### Run All Tests

```bash
pytest
```

### Run Specific Test Categories

```bash
# Unit tests only
pytest tests/unit -v

# Integration tests only
pytest tests/integration -v

# Tests with specific marker
pytest -m unit
pytest -m integration
```

### Run with Coverage

```bash
pytest --cov=checkpcspecs --cov-report=html --cov-report=term
```

The coverage report will be generated in `htmlcov/index.html`.

### Run Specific Test File

```bash
pytest tests/unit/test_models.py -v
```

### Run Specific Test Function

```bash
pytest tests/unit/test_models.py::TestSystemInfo::test_creation -v
```

## Test Fixtures

Common fixtures are defined in `conftest.py`:

- **mock_system_info**: Standard system configuration for testing
- **mock_performance_metrics**: Network performance data
- **mock_low_spec_system**: Low-end system for testing poor ratings
- **mock_high_spec_system**: High-end system for testing excellent ratings

## Test Markers

Tests are marked with the following markers:

- `@pytest.mark.unit`: Unit tests
- `@pytest.mark.integration`: Integration tests
- `@pytest.mark.slow`: Slow-running tests
- `@pytest.mark.network`: Tests requiring network access

## Writing New Tests

### Unit Test Example

```python
import pytest
from checkpcspecs.core.specs_checker import SpecsChecker

class TestNewFeature:
    @pytest.fixture
    def checker(self):
        return SpecsChecker()
    
    def test_something(self, checker):
        result = checker.some_method()
        assert result == expected_value
```

### Integration Test Example

```python
import pytest

class TestIntegration:
    def test_full_workflow(self, mock_system_info):
        # Test complete workflow
        pass
```

## Continuous Integration

Tests run automatically on:
- Push to `main` or `refactor/complete-restructure` branches
- Pull requests to `main`
- Multiple Python versions (3.8 - 3.12)

CI pipeline includes:
1. Linting with flake8
2. Code formatting check with black
3. Import sorting check with isort
4. Type checking with mypy
5. Unit tests with coverage
6. Integration tests

## Coverage Goals

- Overall coverage: > 80%
- Core modules: > 90%
- UI modules: > 70%

## Best Practices

1. **One assertion per test**: Keep tests focused
2. **Use fixtures**: Reuse common setup code
3. **Mock external dependencies**: Don't rely on actual hardware/network
4. **Descriptive names**: Test names should describe what they test
5. **Arrange-Act-Assert**: Follow AAA pattern in tests

## Troubleshooting

### Import Errors

If you get import errors, make sure the package is installed in editable mode:

```bash
pip install -e .
```

### Windows-Specific Tests

Some tests require Windows. Run on Windows or mark as skip:

```python
@pytest.mark.skipif(platform.system() != "Windows", reason="Windows only")
def test_windows_feature():
    pass
```

### Network Tests

Tests marked with `@pytest.mark.network` may fail without internet:

```bash
# Skip network tests
pytest -m "not network"
```
