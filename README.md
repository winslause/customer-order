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

To install all dependencies:
```bash
pip install -r requirements.txt