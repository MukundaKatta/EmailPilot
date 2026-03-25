# Contributing to EmailPilot

Thank you for your interest in contributing to EmailPilot! We welcome contributions from the community.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/<your-username>/EmailPilot.git
   cd EmailPilot
   ```
3. Install development dependencies:
   ```bash
   make install
   ```

## Development Workflow

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes
3. Run checks:
   ```bash
   make check
   ```
4. Commit your changes with a clear message:
   ```bash
   git commit -m "feat: add your feature description"
   ```
5. Push and open a pull request

## Code Style

- We use **black** for formatting and **ruff** for linting
- Run `make format` before committing
- All code must pass `make check`

## Adding Templates

To add a new built-in template:

1. Add it to `BUILTIN_TEMPLATES` in `src/emailpilot/core.py`
2. Add a test in `tests/test_core.py`
3. Update the README template list

## Running Tests

```bash
make test
```

## Reporting Issues

- Use GitHub Issues
- Include a minimal reproducible example
- Describe expected vs. actual behavior

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
