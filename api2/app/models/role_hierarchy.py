from . import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey


class RoleHierarchy(Base):
    __tablename__ = 'role_hierarchy'

    parent_role: Mapped[str] = mapped_column('parent_role',
                                             String(50),
                                             ForeignKey('role.name'),
                                             primary_key=True)
    child_role: Mapped[str] = mapped_column('child_role',
                                            String(50),
                                            ForeignKey('role.name'),
                                            primary_key=True)
