# app/core/config.py
from pydantic_settings import BaseSettings
from pydantic import AnyUrl, Field
import os
from typing import Union

class Base(BaseSettings):
    PORT: int = 8000
    
class Dev(Base):
    #perplexity
    DATABASE_URL: str = Field("postgresql://doadmin:AVNS_v7eSl-1IqkXgEEeTkV3@handyman-db-do-user-28819158-0.d.db.ondigitalocean.com:25060/defaultdb?sslmode=require")
    API_V1_STR: str = Field("/api/v1")
    
class Prod(Base):
    # azureai
    DATABASE_URL: str = Field("postgresql://doadmin:AVNS_v7eSl-1IqkXgEEeTkV3@handyman-db-do-user-28819158-0.d.db.ondigitalocean.com:25060/defaultdb?sslmode=require")
    API_V1_STR: str = Field("/api/v1")

config = dict(
    dev=Dev,
    prod=Prod
)
settings: Union[Dev, Prod] = config[os.environ.get('DEPLOYMENT', 'DEV').lower()]()