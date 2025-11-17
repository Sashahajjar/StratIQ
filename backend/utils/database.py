"""
Database connection and session management
"""

try:
    from sqlalchemy import create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
    from utils.config import settings
    
    # Create database engine (optional - will fail gracefully if DB not available)
    try:
        engine = create_engine(
            settings.DATABASE_URL,
            pool_pre_ping=True,
            echo=settings.ENVIRONMENT == "development"
        )
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    except Exception:
        # Database not available - use in-memory for development
        engine = create_engine("sqlite:///:memory:", echo=False)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Base class for models
    Base = declarative_base()
    
    def get_db():
        """Dependency for getting database session"""
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
except ImportError:
    # SQLAlchemy not installed - provide dummy implementations
    Base = None
    engine = None
    SessionLocal = None
    
    def get_db():
        """Dummy database dependency"""
        yield None

