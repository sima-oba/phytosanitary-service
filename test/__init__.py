class TestConfig:
    """Set Flask configuration variables."""

    TESTING = True

    # General Config
    SECRET_KEY = 'secretkey'
    FLASK_ENV = 'development'
    SERVER_NAME = 'localhost.localdomain'

    # Mongo
    MONGODB_SETTINGS = {
        'db': 'testdb',
        'host': 'localhost',
        'port': 27017,
        'mock': True,
    }

    KAFKA_SERVER = 'localhost:9092'
    KAFKA_GROUP = 'PHYTOSANITARY'
    TOPIC_PHYTOSANITARY = 'PHYTOSANITARY'
    TOPIC_ANNUAL_ORDINANCE = 'ANNUAL_ORDINANCE'

    APM_SERVER_URL = '192.168.1.11'
    APM_SECRET_TOKEN = '12345'
