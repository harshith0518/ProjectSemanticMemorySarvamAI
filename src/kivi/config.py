"""Explicit database configuration; no provider configuration or user input here."""

import os
from dataclasses import dataclass, field
from uuid import UUID

from sqlalchemy import URL

LOCAL_OWNER = UUID("ce9e9be0-bcfa-4d45-b875-6ea50815910a")


@dataclass(frozen=True)
class Settings:
    host: str
    database: str
    user: str
    password: str = field(repr=False)
    port: int = 5432
    environment: str = "development"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            host=os.environ["KIVI_DB_HOST"],
            database=os.environ["KIVI_DB_NAME"],
            user=os.environ["KIVI_DB_USER"],
            password=os.environ["KIVI_DB_PASSWORD"],
            port=int(os.environ.get("KIVI_DB_PORT", "5432")),
            environment=os.environ.get("KIVI_ENV", "development"),
        )

    @property
    def url(self) -> URL:
        return URL.create(
            "postgresql+psycopg",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
        )

    def require_test_database(self) -> None:
        # Fail closed before migration, cleanup, or fixture writes.
        if (
            self.environment != "test"
            or self.host != "test-db"
            or self.port != 5432
            or self.database != "kivi_test"
            or self.user not in {"kivi_test_app", "kivi_test_migrate"}
        ):
            raise ValueError("Database checks require the isolated Compose test database")
