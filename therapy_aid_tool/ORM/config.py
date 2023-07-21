import dotenv
import os
import pymysql

pymysql.install_as_MySQLdb()

dotenv.load_dotenv()

SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
