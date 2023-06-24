from pydantic import BaseSettings

class Settings(BaseSettings):
    db_hostname:str
    db_password:str
    db_username:str
    db_name:str
    db_port:str
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SECRET_KEY:str
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return f"mysql+pymysql://{self.db_username}:{self.db_password}@{self.db_hostname}:{self.db_port}/{self.db_name}"
        
    class Config:
        env_file = ".env"
        

settings=Settings()