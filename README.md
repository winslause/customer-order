# Customer Order API

A Django-based web application for managing customers and orders, featuring OpenID Connect (OIDC) authentication via Auth0, SMS notifications using Africa's Talking, and a responsive UI with Bootstrap. The project includes a REST API, unit tests, a CI/CD pipeline with GitHub Actions.

## Features
- **REST API**: Programmatically manage customers and orders.
- **Authentication**: Secure OIDC login/logout using Auth0.
- **SMS Notifications**: Send SMS alerts via Africa's Talking when new orders are created.
- **Responsive UI**: Built with Bootstrap 5, Google Fonts (Roboto), and custom CSS/JS with a sticky footer.
- **Testing**: Unit tests with coverage for core functionality.
- **CI/CD**: Automated testing and deployment via GitHub Actions and Heroku.

## Tech Stack
- **Backend**: Django 5.0.6, Python 3.11
- **Database**: SQLite (development and production)
- **Frontend**: Bootstrap 5, Google Fonts (Roboto), custom CSS/JS
- **Authentication**: Auth0 with `mozilla-django-oidc`
- **SMS Service**: Africa's Talking
- **CI/CD**: GitHub Actions

## Installed Packages
The project uses the following packages (from `requirements.txt`):
- **django==5.0.6**: Web framework.
- **django-environ==0.11.2**: Environment variable management.
- **mozilla-django-oidc==4.0.0**: OIDC authentication with Auth0.
- **requests==2.32.3**: HTTP requests for SMS integration.
- **python-decouple==3.8**: Configuration management.
- **coverage==7.6.1**: Test coverage reporting.
- **gunicorn==23.0.0**: WSGI server for production.
- **whitenoise==6.7.0**: Static file serving in production.
- **africastalking==1.2.6**: Africa's Talking SMS API client.

"""
**
africastalking==1.2.6
asgiref==3.8.1
attrs==25.3.0
certifi==2025.4.26
cffi==1.17.1
charset-normalizer==3.4.2
coverage==7.6.1
cryptography==45.0.3
Django==5.0.6
django-environ==0.11.2
django-js-asset==3.1.2
django-mptt==0.17.0
djangorestframework==3.16.0
drf-spectacular==0.28.0
gunicorn==23.0.0
idna==3.10
inflection==0.5.1
josepy==2.0.0
jsonschema==4.24.0
jsonschema-specifications==2025.4.1
mozilla-django-oidc==2.0.0
packaging==25.0
pycparser==2.22
python-decouple==3.8
PyYAML==6.0.2
referencing==0.36.2
requests==2.32.3
rpds-py==0.25.1
schema==0.7.7
sqlparse==0.5.3
typing_extensions==4.13.2
tzdata==2025.2
uritemplate==4.1.1
urllib3==2.4.0
whitenoise==6.7.0

**
"""

To install all dependencies:
```bash
pip install -r requirements.txt