# Contributing to Local Store E-commerce

First off, thank you for considering contributing to Local Store! It's people like you that make this project better for everyone.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** to demonstrate the steps
- **Describe the behavior you observed** and what you expected to see
- **Include screenshots** if applicable
- **Include your environment details** (OS, Python version, Django version)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Use a clear and descriptive title**
- **Provide a detailed description** of the suggested enhancement
- **Explain why this enhancement would be useful**
- **List any similar features** in other applications if applicable

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following our coding standards
3. **Test your changes** thoroughly
4. **Update documentation** if needed
5. **Write clear commit messages**
6. **Submit a pull request**

## Development Setup

### Prerequisites
- Python 3.8 or higher
- pip
- virtualenv (recommended)

### Setting Up Your Development Environment

1. **Fork and clone the repository**
```bash
git clone https://github.com/yourusername/Local_Store_ecommerce.git
cd Local_Store_ecommerce
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Create a superuser**
```bash
python manage.py createsuperuser
```

6. **Run the development server**
```bash
python manage.py runserver
```

## Coding Standards

### Python Code Style
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused
- Maximum line length: 100 characters

### Django Best Practices
- Use Django's built-in features when possible
- Follow Django's naming conventions
- Use class-based views for complex views
- Keep business logic in models
- Use Django forms for data validation

### HTML/CSS/JavaScript
- Use semantic HTML5 elements
- Follow BEM naming convention for CSS classes
- Keep JavaScript modular and well-commented
- Ensure responsive design
- Test on multiple browsers

### Git Commit Messages
- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters
- Reference issues and pull requests when applicable

Example:
```
Add product wishlist feature

- Create Wishlist model
- Add wishlist views and templates
- Update user profile to show wishlist
- Add tests for wishlist functionality

Closes #123
```

## Testing

### Running Tests
```bash
python manage.py test
```

### Writing Tests
- Write tests for new features
- Ensure existing tests pass
- Aim for good test coverage
- Test both success and failure cases

## Documentation

- Update README.md if you change functionality
- Update FEATURES.md for new features
- Add docstrings to new functions and classes
- Update API documentation if applicable

## Project Structure

```
Local_Store_ecommerce/
├── localstore/          # Project settings
├── store/               # Main application
│   ├── models.py        # Database models
│   ├── views.py         # View functions
│   ├── urls.py          # URL routing
│   ├── admin.py         # Admin configuration
│   ├── templates/       # HTML templates
│   └── tests/           # Test files
├── static/              # Static files (CSS, JS)
├── media/               # User uploads
└── requirements.txt     # Dependencies
```

## Feature Development Workflow

1. **Create an issue** describing the feature
2. **Get feedback** from maintainers
3. **Create a branch** for your feature
4. **Develop the feature** following coding standards
5. **Write tests** for your feature
6. **Update documentation**
7. **Submit a pull request**
8. **Address review comments**
9. **Merge** after approval

## Database Migrations

When making model changes:

1. **Create migrations**
```bash
python manage.py makemigrations
```

2. **Review the migration file**
```bash
python manage.py sqlmigrate store 0001
```

3. **Apply migrations**
```bash
python manage.py migrate
```

4. **Commit migration files** with your changes

## Static Files

When modifying CSS or JavaScript:

1. **Make changes** in the `static/` directory
2. **Test locally** with `python manage.py runserver`
3. **Collect static files** for production:
```bash
python manage.py collectstatic
```

## Questions?

Feel free to:
- Open an issue for questions
- Join our discussions
- Contact the maintainers

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing! 🎉
