"""
QuickAI Ideas Configuration
This file includes necessary configuration settings for the QuickAI Ideas application.

To use, replace placeholders with your actual API keys and proper settings.
"""

# General configuration for the application
class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = "replace_with_your_secret_key"

# Development environment settings
class DevelopmentConfig(Config):
    DEBUG = True
    GPT3_API_KEY = "replace_with_your_gpt3_api_key_in_dev"
    WORDPRESS_REST_API_URL = "http://localhost/your_wordpress_site/wp-json"
    WORDPRESS_USERNAME = "your_wordpress_username"
    WORDPRESS_APPLICATION_PASSWORD = "your_wordpress_application_password_in_dev"

# Testing environment settings
class TestingConfig(Config):
    TESTING = True
    GPT3_API_KEY = "replace_with_your_gpt3_api_key_in_test"
    WORDPRESS_REST_API_URL = "http://test.your_wordpress_site/wp-json"
    WORDPRESS_USERNAME = "your_test_wordpress_username"
    WORDPRESS_APPLICATION_PASSWORD = "your_wordpress_application_password_in_test"

# Production environment settings
class ProductionConfig(Config):
    GPT3_API_KEY = "replace_with_your_gpt3_api_key_in_prod"
    WORDPRESS_REST_API_URL = "http://your_wordpress_site.com/wp-json"
    WORDPRESS_USERNAME = "your_wordpress_username"
    WORDPRESS_APPLICATION_PASSWORD = "your_wordpress_application_password_in_prod"

# Environment specific configurations
config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}

def get_config_by_name(env_name):
    return config_by_name.get(env_name, DevelopmentConfig)
    