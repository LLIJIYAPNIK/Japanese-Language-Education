from backend.database import SessionLocal
from backend.services.crud import CRUDBase
from backend.models import Translation, Word, word_translation

from sqlalchemy import and_, select, insert

word_crud = CRUDBase[Word](Word)
translation_crud = CRUDBase[Translation](Translation)


async def add_word_translation_link(
        session: SessionLocal,
        kanji: str,
        kana: str,
        translation_text: str,
        rating: float
) -> Word | None:
    try:
        translation = await translation_crud.find_one(
            session,
            Translation.text == translation_text
        )

        if not translation:
            translation = await translation_crud.create(
                session,
                text=translation_text,
            )

        word = await word_crud.find_one(
            session,
            and_(Word.kanji == kanji, Word.kana == kana)
        )

        if not word:
            word = await word_crud.create(
                session,
                kanji=kanji,
                kana=kana,
                rating=rating
            )

        result = await session.execute(
            select(word_translation)
            .where(and_(
                (word_translation.c.word_id == word.id),
                (translation.c.id == translation.id)
            ))
        )

        if not result.scalar():
            await session.execute(
                insert(word_translation)
                .values(
                    word_id=word.id,
                    translation_id=translation.id
                )
            )

        return word
    except Exception:
        await session.rollback()
        raise
