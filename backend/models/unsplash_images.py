from backend.database import Base

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class UnsplashImages(Base):
    __tablename__ = 'unsplash_images'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    image_id: Mapped[int] = mapped_column(String)
    image_regular_url: Mapped[String] = mapped_column(String, unique=True)
    image_small_url: Mapped[String] = mapped_column(String, unique=True)
