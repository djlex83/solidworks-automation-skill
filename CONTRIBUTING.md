# Contributing to SolidWorks Automation Skill

Thank you for your interest in contributing!

## How to Contribute

### Reporting Bugs

1. Check if the issue already exists
2. Create a new issue with:
   - SolidWorks version
   - Python version
   - Error message/traceback
   - Steps to reproduce

### Suggesting Features

1. Open an issue describing the feature
2. Explain the use case
3. Provide examples if possible

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test with SolidWorks
5. Commit (`git commit -m 'Add amazing feature'`)
6. Push (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Code Style

- Use Python type hints where possible
- Document functions with docstrings
- Keep methods focused and small
- Add examples for new features

## Adding New Operations

### New Sketch Operation

1. Add method to `SketchOperations` class in `sw_automation.py`
2. Document in `references/sketch-operations.md`
3. Add example to `references/examples.md`

### New Feature Operation

1. Add method to `FeatureOperations` class in `sw_automation.py`
2. Document in `references/feature-operations.md`
3. Add example to `references/examples.md`

## Testing

Since this requires SolidWorks (Windows only), please test your changes manually:

1. Start SolidWorks
2. Open a new Part
3. Run your code
4. Verify the result in SolidWorks

## Questions?

Open an issue for any questions!
