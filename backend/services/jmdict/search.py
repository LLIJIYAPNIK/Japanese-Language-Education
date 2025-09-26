from backend.shared import word_in_translation

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from backend.models import Translation, Word


async def search_words_by_translation(
        session,
        search_term: str,
        limit: int = 10
) -> list[dict]:
    normalize_term = search_term.lower().strip()

    result = await session.execute(
        select(Translation)
        .options(
            joinedload(Translation.words)
            .joinedload(Word.translations)
        )
    )
    translations = result.unique().scalars().all()

    matched_words = []
    for translation in translations:
        found, priority = word_in_translation(normalize_term, translation.text)
        if found:
            for word in translation.words:
                word_data = {
                    "id": word.id,
                    "kanji": word.kanji,
                    "kana": word.kana,
                    "rating": word.rating,
                    "translations": [t.text for t in word.translations],
                    "matched_translations": translation.text,
                    "priority": priority
                }
                matched_words.append(word_data)

    seen = set()
    unique_words = []

    for word in matched_words:
        key = (word["kanji"], word["kana"])
        if key not in seen:
            seen.add(key)
            unique_words.append(word)

    sorted_words = sorted(
        unique_words,
        key=lambda x: (x["priority"], x["rating"]),
        reverse=True
    )
    return sorted_words[:limit]
