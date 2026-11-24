"""创建账号表并授予运行角色最小权限。"""

import sqlalchemy as sa
from alembic import op

revision = "0001_admin_account"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """创建账号表并授权读取账号和更新当前会话。"""
    op.create_table(
        "admin_account",
        sa.Column("admin_account_id", sa.Uuid(), primary_key=True),
        sa.Column("account", sa.String(128), nullable=False, unique=True),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("password_hash", sa.Text(), nullable=False),
        sa.Column("role", sa.String(32), nullable=False),
        sa.Column("session_id", sa.Uuid()),
        sa.CheckConstraint(
            "role IN ('admin', 'super_admin')",
            name="ck_admin_account_role",
        ),
        schema="admin_auth",
    )
    op.execute("GRANT USAGE ON SCHEMA admin_auth TO admin_login")
    op.execute("GRANT SELECT, UPDATE (session_id) ON admin_auth.admin_account TO admin_login")


def downgrade() -> None:
    """删除本次迁移创建的账号表。"""
    op.drop_table("admin_account", schema="admin_auth")
