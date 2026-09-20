from sqlalchemy import create_engine, text

from ..models import User

class DatabaseClient:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.engine = create_engine(db_url)

    def execute_query(self, query: str):
        with self.engine.begin() as connection:
            result = connection.execute(text(query))
            return result.fetchall()
        
    def add_user(self, user: User):
        with self.engine.begin() as connection:
            connection.execute(
                text("INSERT INTO users (email, created_at, updated_at, password_hash, is_active, username, first_name, last_name) VALUES (:email, :created_at, :updated_at, :password_hash, :is_active, :username, :first_name, :last_name)"),
                {
                    "email": user.email,
                    "created_at": user.created_at,
                    "updated_at": user.updated_at,
                    "password_hash": User.hash_password(user.password_hash),
                    "is_active": user.is_active,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name
                }
            )
            
    def get_user_by_id(self, user_id: int) -> User | None:
        with self.engine.begin() as connection:
            result = connection.execute(
                text("SELECT * FROM users WHERE id = :id"),
                {"id": user_id}
            ).fetchone()

            if result is None:
                return None

            return User(
                id=result.id,
                email=result.email,
                created_at=result.created_at,
                updated_at=result.updated_at,
                password_hash=result.password_hash,
                is_active=result.is_active,
                username=result.username,
                first_name=result.first_name,
                last_name=result.last_name
            )

    def revoke_token(self, jti: str, expires_at) -> None:
        with self.engine.begin() as connection:
            connection.execute(text("DELETE FROM revoked_tokens WHERE expires_at < NOW()"))
            connection.execute(
                text("INSERT INTO revoked_tokens (jti, expires_at) VALUES (:jti, :expires_at) ON CONFLICT (jti) DO NOTHING"),
                {"jti": jti, "expires_at": expires_at}
            )

    def is_token_revoked(self, jti: str) -> bool:
        with self.engine.begin() as connection:
            result = connection.execute(
                text("SELECT 1 FROM revoked_tokens WHERE jti = :jti"),
                {"jti": jti}
            ).fetchone()
            return result is not None

    def validate_user(self, email: str, password: str) -> User | None:
        with self.engine.begin() as connection:
            result = connection.execute(
                text("SELECT * FROM users WHERE email = :email"),
                {"email": email}
            ).fetchone()
            
            if result is None:
                return None
            
            user = User(
                id=result.id,
                email=result.email,
                created_at=result.created_at,
                updated_at=result.updated_at,
                password_hash=result.password_hash,
                is_active=result.is_active,
                username=result.username,
                first_name=result.first_name,
                last_name=result.last_name
            )
            
            if user.verify_password(password):
                return user
            
            return None