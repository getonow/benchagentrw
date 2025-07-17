import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database Configuration
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/benchagent")
    
    # Supabase Configuration
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
    
    # File Paths
    SPECS_DIRECTORY = os.getenv("SPECS_DIRECTORY", "./SPECS")
    
    # Web Scraping Configuration
    MAX_ALTERNATIVE_SUPPLIERS = int(os.getenv("MAX_ALTERNATIVE_SUPPLIERS", "5"))
    WEB_SCRAPING_TIMEOUT = int(os.getenv("WEB_SCRAPING_TIMEOUT", "30"))
    
    # API Configuration
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8099"))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    # Google Custom Search API
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

config = Config() 