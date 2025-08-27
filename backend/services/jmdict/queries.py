from backend.models import Word, Translation, word_translation

from sqlalchemy import select


async def get_translations_by_word(
        session,
        kana: str,
        kanji: str | None = None,
) -> dict | None:
    stmt = select(Word).where(Word.kana == kana)
    if kanji:
        stmt = stmt.where(Word.kana == kanji)

    result = await session.execute(stmt)
    word = result.scalar_one_or_none()

    if not word:
        return None

    result = await session.execute(
        select(Translation)
        .join(word_translation)
        .where(word_translation.c.word_id == word.id)
    )
    translations = result.scalars().all()

    return {
        "word": {
            "id": word.id,
            "kana": word.kana,
            "kanji": word.kanji,
            "rating": word.rating
        },
        "translations": [t.text for t in translations]
    }
