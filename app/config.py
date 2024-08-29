class Config:
    """
    Configuration class for setting up the app's configurations.

    Attributes:
        SQLALCHEMY_DATABASE_URI (str): The database URI that SQLAlchemy will use for the application.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): A flag to disable or enable SQLAlchemy's track modifications feature.
        JWT_SECRET_KEY (str): The secret key used for signing JSON Web Tokens (JWT) for authentication.
    """

    SQLALCHEMY_DATABASE_URI: str = 'sqlite:///app.db'
    # The URI for the SQLite database. The application will use this database for storing data.

    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    # This flag disables the SQLAlchemy event system, which is not needed and consumes extra memory.

    JWT_SECRET_KEY: str = 'cloudSEK-intern-task'
    # The secret key used to sign JWT tokens. It is crucial for the security of the token generation and verification process.
