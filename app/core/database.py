"""定义账号表及 PostgreSQL 连接。"""

import sqlalchemy as sa
from sqlalchemy.engine import Engine, make_url

AUTH_SCHEMA = "admin_auth"
ROLES = ("admin", "super_admin")
account_table = sa.Table(
    "admin_account",
    sa.MetaData(),
    sa.Column("admin_account_id", sa.Uuid(), primary_key=True),
    sa.Column("account", sa.String(128)),
    sa.Column("name", sa.String(128)),
    sa.Column("password_hash", sa.Text()),
    sa.Column("role", sa.String(32)),
    sa.Column("session_id", sa.Uuid()),
    schema=AUTH_SCHEMA,
)


def database_engine(url: str) -> Engine:
    """创建延迟连接的 PostgreSQL 引擎。

    Args:
        url: PostgreSQL 连接地址，允许省略 psycopg 驱动名。
    """
    parsed = make_url(url)
    if parsed.drivername not in {"postgresql", "postgresql+psycopg"}:
        raise ValueError("数据库 URL 必须使用 PostgreSQL 和 psycopg。")
    return sa.create_engine(
        parsed.set(drivername="postgresql+psycopg"),
        pool_pre_ping=True,
        connect_args={"connect_timeout": 3},
    )
