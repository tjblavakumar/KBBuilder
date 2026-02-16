# Contributing to KB Builder

Thank you for your interest in contributing to KB Builder!

## How to Contribute

### Reporting Issues

- Use GitHub Issues to report bugs
- Include detailed steps to reproduce
- Provide error messages and logs
- Mention your OS and Python/Node versions

### Suggesting Features

- Open an issue with the "enhancement" label
- Describe the feature and use case
- Explain why it would be useful

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages
6. Push to your fork
7. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/KBBuilder.git
cd KBBuilder

# Backend setup
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

# Frontend setup
cd frontend
npm install --legacy-peer-deps
cd ..

# Start development
./start-simple.sh
```

## Code Style

### Python
- Follow PEP 8
- Use type hints
- Add docstrings to functions
- Keep functions focused and small

### JavaScript/Vue
- Use ES6+ features
- Follow Vue 3 Composition API style
- Use meaningful variable names
- Add comments for complex logic

## Testing

Before submitting:
- Test with both OpenAI and Bedrock (if possible)
- Check for console errors
- Verify API endpoints work
- Test edge cases

## Adding New LLM Providers

The architecture makes it easy to add new providers:

1. Create provider class in `backend/services/`
2. Implement `LLMProvider` interface
3. Add to factory function in `llm_provider.py`
4. Update frontend provider dropdown
5. Add documentation

See [Architecture Diagram](docs/ARCHITECTURE_DIAGRAM.md) for details.

## Documentation

- Update README.md for user-facing changes
- Add technical details to docs/
- Include code examples
- Update configuration examples

## Questions?

Open an issue or discussion on GitHub!

Thank you for contributing! 🎉
