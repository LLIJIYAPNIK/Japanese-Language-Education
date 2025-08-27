from backend.database import Base

from sqlalchemy import Integer, Table, ForeignKey, Column

word_translation = Table(
    "word_translation",
    Base.metadata,
    Column("word_id", Integer, ForeignKey("words.id"), primary_key=True),
    Column("translation_id", Integer, ForeignKey("translations.id"), primary_key=True)
)
