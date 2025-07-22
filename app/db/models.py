import datetime
from zoneinfo import ZoneInfo
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import table_registry

def now_sp():
    return datetime.datetime.now(ZoneInfo("America/Sao_Paulo"))

@table_registry.mapped_as_dataclass
class UserModel():
    __tablename__ = 'users'
    id : Mapped[int] = mapped_column(nullable=False, primary_key=True, init=False)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(init=False, default=now_sp())
    updated_at: Mapped[datetime.datetime] = mapped_column(init=False, default=now_sp(), onupdate= now_sp())


# depois preciso dar um alembic init migrations