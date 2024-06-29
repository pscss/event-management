import re

from sqlalchemy import Column
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, as_declarative
from sqlalchemy.sql.sqltypes import Integer


def camel_case_split(word: str):
    return re.findall(r"[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))", word)


@as_declarative()
class Base:
    def __init__(self, *args, **kwargs) -> None: ...  # noqa

    id: Mapped[int] = Column(  # type:ignore
        Integer, primary_key=True, index=True
    )

    __name__: str

    @declared_attr
    def __tablename__(cls) -> Mapped[str]:
        """Split current classname by camelcase and
        return the joined word by underscore."""
        return "_".join(camel_case_split(cls.__name__)).lower()  # type:ignore
