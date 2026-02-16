# Pre-Commit Checklist

Before committing to GitHub, verify:

## ✅ Sensitive Data Removed

- [ ] No API keys in code
- [ ] `backend/config.yml` is gitignored (not committed)
- [ ] No database files (*.db) committed
- [ ] No log files committed
- [ ] No personal data in test files

## ✅ Files Cleaned Up

- [ ] Unnecessary documentation removed
- [ ] Temporary files deleted
- [ ] Only essential files in root
- [ ] Documentation organized in docs/

## ✅ Configuration

- [ ] `config.example.yml` has placeholder values
- [ ] `.gitignore` is up to date
- [ ] README.md is complete and accurate

## ✅ Code Quality

- [ ] No debug print statements (or commented out)
- [ ] No commented-out code blocks
- [ ] Proper error handling
- [ ] Code is formatted consistently

## ✅ Documentation

- [ ] README.md is clear and complete
- [ ] Setup instructions are accurate
- [ ] All features are documented
- [ ] Links work correctly

## ✅ Testing

- [ ] Application starts successfully
- [ ] Can create a knowledge base
- [ ] Can chat with KB
- [ ] No console errors
- [ ] Both providers work (if configured)

## 🔍 Final Checks

```bash
# Check for sensitive data
grep -r "sk-proj-" . --exclude-dir=venv --exclude-dir=node_modules --exclude-dir=.git

# Check for API keys
grep -r "api_key.*sk-" . --exclude-dir=venv --exclude-dir=node_modules --exclude-dir=.git

# Verify gitignore
git status --ignored

# Check what will be committed
git status
```

## 📝 Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Tests
- `chore`: Maintenance

Example:
```
feat: Add OpenAI provider support

- Implemented OpenAI LLM provider
- Added config file system for API keys
- Updated UI to support provider selection

Closes #123
```

## 🚀 Ready to Commit!

Once all checks pass:

```bash
git add .
git commit -m "Your message here"
git push origin main
```
