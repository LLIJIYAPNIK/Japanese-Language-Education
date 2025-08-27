from backend.database import Base

from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.types import String, Integer


class Translation(Base):
    __tablename__ = "translations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)

    words: Mapped[list["Word"]] = relationship(
        "Word",
        secondary="word_translation",
        back_populates="translations"
    )
