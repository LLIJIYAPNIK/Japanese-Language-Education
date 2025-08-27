from backend.database import Base

from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.types import String, Integer, Float


class Word(Base):
    __tablename__ = "words"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    kanji: Mapped[str] = mapped_column(String)
    kana: Mapped[str] = mapped_column(String, nullable=False, index=True)
    rating: Mapped[float] = mapped_column(Float, nullable=False, index=True)

    # Связь many-to-many
    translations: Mapped[list["Translation"]] = relationship(
        "Translation",
        secondary="word_translation",
        back_populates="words"
    )