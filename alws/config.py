import urllib.parse
from typing import Annotated, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    pulp_host: str = 'http://pulp'
    pulp_user: str = 'admin'
    pulp_password: str = 'admin'
    pulp_export_path: str = '/srv/exports'
    pulp_database_url: str = (
        'postgresql+psycopg2://postgres:password@pulp:5432/pulp'
    )
    pulp_async_database_url: str = (
        'postgresql+asyncpg://postgres:password@pulp:5432/pulp'
    )

    alts_host: str = 'http://alts-scheduler:8000'
    alts_token: str
    gitea_host: str = 'https://git.almalinux.org/api/v1/'

    package_beholder_enabled: bool = True
    beholder_host: str = 'http://beholder-web:5000'
    beholder_token: Optional[str] = None

    redis_url: str = 'redis://redis:6379'

    database_url: str = 'postgresql+asyncpg://postgres:password@db/almalinux-bs'
    test_database_url: str = (
        'postgresql+asyncpg://postgres:password@db/test-almalinux-bs'
    )
    sync_database_url: str = (
        'postgresql+psycopg2://postgres:password@db/almalinux-bs'
    )

    fastapi_sqla__async__sqlalchemy_url: str = (
        'postgresql+asyncpg://postgres:password@db/almalinux-bs'
    )
    fastapi_sqla__async__sqlalchemy_echo_pool: bool = True

    sqlalchemy_url: str = (
        'postgresql+psycopg2://postgres:password@db/almalinux-bs'
    )
    sqlalchemy_pool_pre_ping: bool = True
    sqlalchemy_pool_recycle: int = 3600

    fastapi_sqla__pulp__sqlalchemy_url: str = (
        'postgresql+psycopg2://postgres:password@pulp:5432/pulp'
    )
    fastapi_sqla__pulp__sqlalchemy_pool_pre_ping: bool = True
    fastapi_sqla__pulp__sqlalchemy_pool_recycle: int = 3600

    fastapi_sqla__pulp_async__sqlalchemy_url: str = (
        'postgresql+asyncpg://postgres:password@pulp:5432/pulp'
    )
    fastapi_sqla__pulp_async__sqlalchemy_echo_pool: bool = True

    github_client: str
    github_client_secret: str

    almalinux_client: str = 'secret'
    almalinux_client_secret: str = 'secret'

    jwt_secret: str
    jwt_algorithm: str = 'HS256'

    immudb_username: Optional[str] = None
    immudb_password: Optional[str] = None
    immudb_database: Optional[str] = None
    immudb_address: Optional[str] = None
    immudb_public_key_file: Optional[str] = None

    rabbitmq_default_user: str = 'test-system'
    rabbitmq_default_pass: str = 'test-system'
    rabbitmq_default_host: str = 'rabbitmq'
    rabbitmq_default_vhost: str = 'test_system'

    albs_api_url: Optional[str] = 'http://web_server:8000/api/v1/'
    albs_jwt_token: Optional[str] = None

    sign_server_api_url: Optional[str] = 'http://sign_file:8000/'
    sign_server_username: Optional[str] = None
    sign_server_password: Optional[str] = None
    test_sign_key_id: Optional[str] = None

    documentation_path: str = 'alws/documentation/'

    logging_level: Optional[str] = 'INFO'

    frontend_baseurl: Annotated[str, Field(validate_default=True)] = (
        'http://localhost:8080'
    )
    github_callback_endpoint: str = 'api/v1/auth/github/callback'
    almalinux_callback_endpoint: str = 'api/v1/auth/almalinux/callback'

    sentry_environment: str = 'dev'
    sentry_dsn: Optional[str] = None
    sentry_traces_sample_rate: float = 0.2

    github_integration_enabled: bool = False
    github_app_id: Optional[str] = None
    path_to_github_app_pem: Optional[str] = None
    github_installation_id: Optional[str] = None
    github_token: Optional[str] = None
    github_organization_name: str = 'AlmaLinux'
    github_project_number: Optional[int] = None
    github_default_repository_name: str = 'updates'

    @field_validator('frontend_baseurl')
    @classmethod
    def validate_frontend_url(cls, value: str) -> str:
        if not value.endswith('/'):
            value += '/'
        return value

    @property
    def codenotary_enabled(self) -> bool:
        return bool(self.immudb_username) and bool(self.immudb_password)

    @property
    def github_callback_url(self) -> str:
        return urllib.parse.urljoin(
            settings.frontend_baseurl,
            settings.github_callback_endpoint,
        )

    @property
    def almalinux_callback_url(self) -> str:
        return urllib.parse.urljoin(
            settings.frontend_baseurl,
            settings.almalinux_callback_endpoint,
        )


settings = Settings()
