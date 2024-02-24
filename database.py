from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv, dotenv_values

load_dotenv()
config = dotenv_values(".env")
#print(config["SERVER_USER"])

# SERVER_USER, SERVER_PASSWORD, URL, DB_NAME = config

#TODO: compare orm to python architecture book & update

# Connect to DB
# postgresql://username:password@server/database
engine = create_engine(
    f'postgresql://{config["SERVER_USER"]}:{config["SERVER_PASSWORD"]}@{config["URL"]}/{config["DB_NAME"]}',
    echo=True
)

Base = declarative_base()

# The sessionmaker factory generates new Session objects when called
#Session = sessionmaker()
Session = sessionmaker(engine)

