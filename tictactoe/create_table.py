from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, create_engine

Base = declarative_base()
engine = create_engine('sqlite:///games.db')
Session = sessionmaker(bind=engine)
session = Session()

class Game(Base):
    __tablename__ = 'tic_tac_toe'

    id = Column(Integer, primary_key=True)
    player_name = Column(String)
    player_wins = Column(Integer)
    player_losses = Column(Integer)
    player_draws = Column(Integer)


    def __init__(self, player_name, player_wins, player_losses, player_draws):
        self.player_name = player_name
        self.player_wins = player_wins
        self.player_losses = player_losses
        self.player_draws = player_draws


Base.metadata.create_all(engine) 



