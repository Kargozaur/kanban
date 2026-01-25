from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["argon2"],
    argon2__time_cost=3,
    arogn2__memory_cost=65536,
    argon2__parallelism=2,
)


class PasswordHasher:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(password: str, db_password: str) -> bool:
        return pwd_context.verify(password, db_password)


def get_hasher():
    return PasswordHasher
