from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import logging
db=SQLAlchemy()
jwt=JWTManager()


# Configuring Logging
logging.basicConfig(
    filename="logs/app.log",  #this directory to save logging
    level=logging.INFO,  # Log INFO and above (WARNING, ERROR)
    format="%(asctime)s - %(levelname)s - %(message)s",  #this is the Log format
)
logger = logging.getLogger(__name__)