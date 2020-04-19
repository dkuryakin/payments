from pydantic import BaseSettings, RedisDsn as _RedisDsn, PostgresDsn


class RedisDsn(_RedisDsn):
    # There is known issue with RedisDsn for pydantic:
    # https://github.com/samuelcolvin/pydantic/issues/1275
    # And it's still not solved, so make own temporary fix.
    user_required = False


class Settings(BaseSettings):
    title: str
    version: str
    loglevel: str
    decimal_precision: int
    default_transfer_fee: float
    postgres_dsn: PostgresDsn
    redis_dsn: RedisDsn
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_lifetime_seconds: int
    token_url: str
    origins: str

    class Config:
        env_prefix = 'PAYMENTS_'


settings = Settings()
