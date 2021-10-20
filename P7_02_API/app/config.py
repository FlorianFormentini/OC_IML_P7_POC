import os

basedir = os.getcwd()


class Config(object):
    """Base config"""
    DEBUG = False
    TESTING = False

    # API
    SECRET_KEY = 'dev_apikey'
    RESTX_MASK_SWAGGER = True
    ERROR_404_HELP = False  # disable complementary error message when 404

    # Database
    MONGODB_HOST = os.getenv('MONGODB_URI', 'localhost:27017')

    # File upload
    ALLOWED_EXT = {'jpg', 'png', 'jpeg', 'json'}
    UPLOAD_DIR = os.path.join(os.getcwd(), 'tmp')

    # Facebook
    FB_VERIFY_TOKEN = os.getenv('FB_VERIFY_TOKEN')
    FB_PAGE_ACCESS_TOKEN = os.getenv('FB_PAGE_ACCESS_TOKEN')
    FB_SEND_API_URL = 'https://graph.facebook.com/v10.0/me/messages'

    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_TOKEN')
    TELEGRAM_BOT_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

    # # GoogleCloudPlatform
    # GOOGLE_APPLICATION_CREDENTIALS = os.getenv(
    #     'GOOGLE_APPLICATION_CREDENTIALS')
    # CLOUD_STORAGE_BUCKET = 'heraproject-us'

    # Chatbot
    CHATBOT_PATH = {
        'vectorizer_responses': 'app/static/fitted-preprocessor.pkl',
        'model': 'app/static/fitted-model.h5'
    }
    PRED_THRESHOLD = .6


class DevelopmentConfig(Config):
    """Uses local database server and display debug"""
    DEBUG = True
    # UPLOAD_DIR = os.path.join(basedir.parent, 'Uploads')
    HOST_URL = os.getenv('LOCAL_HOST_URL', 'http://localhost:5000')


class ProductionConfig(Config):
    """Uses production database server"""
    DEBUG = False
    HOST_URL = os.getenv('PROD_HOST_URL')
    SECRET_KEY = os.getenv('API_KEY')


class TestingConfig(Config):
    """Unit tests configuration"""
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    API_KEY = os.getenv('API_KEY', 'test_apikey')


config_by_name = {
    'dev': DevelopmentConfig,
    'development': DevelopmentConfig,
    'test': TestingConfig,
    'tests': TestingConfig,
    'prod': ProductionConfig,
    'production': ProductionConfig,
}
