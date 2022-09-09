import logging
import os
import dotenv
import logging.config


dotenv.load_dotenv()


class Config:
    KAFKA_SERVER = os.getenv('KAFKA_SERVER')
    MONGODB_SETTINGS = {
        'db': os.environ['MONGO_DB'],
        'host': os.environ['MONGO_HOST'],
        'port': os.getenv('MONGO_PORT', '27017'),
        'username': os.environ['MONGO_USER'],
        'password': os.environ['MONGO_PASSWORD'],
        'authentication_source': 'admin',
    }
    INTROSPECTION_URI = os.getenv('INTROSPECTION_URI')
    LOG_DIR = os.getenv('LOG_DIR', './logs')


# Set up logging
if not os.path.exists(Config.LOG_DIR):
    os.mkdir(Config.LOG_DIR)

if not os.path.isdir(Config.LOG_DIR):
    raise ValueError(f'{Config.LOG_DIR} is not a directory')

logging.config.fileConfig('./logging.ini')
