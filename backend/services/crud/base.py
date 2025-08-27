from sqlalchemy.engine import ScalarResult
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update as sql_update, delete as sql_delete, CursorResult

from typing import Generic, TypeVar, Type, Sequence

T = TypeVar('T')


class CRUDBase(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    async def create(self, session: AsyncSession, **data) -> T:
        obj = self.model(**data)
        session.add(obj)
        await session.flush()
        return obj

    async def get_by_id(self, session: AsyncSession, id: int) -> T | None:
        result = await session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def find_one(self, session: AsyncSession, *condition) -> T | None:
        result = await session.execute(
            select(self.model).where(*condition)
        )
        return result.scalar_one_or_none()

    async def find_many(self, session: AsyncSession, *condition) -> Sequence[T]:
        result = await session.execute(
            select(self.model).where(*condition)
        )
        scalars: ScalarResult[T] = result.scalars()
        return scalars.all()

    async def update_one(self, session: AsyncSession, id: int, **data) -> bool:
        try:
            result: CursorResult = await session.execute(
                sql_update(self.model)
                .where(self.model.id == id)
                .values(**data)
                .execution_options(synchronize_session="fetch")
            )
            await session.commit()
            return result.rowcount > 1
        except SQLAlchemyError:
            await session.rollback()
            return False

    async def update_many(self, session: AsyncSession, ids: list[int], **data) -> bool:
        if not ids:
            return True

        try:
            result: CursorResult = await session.execute(
                sql_update(self.model)
                .where(self.model.id.in_(ids))
                .values(**data)
                .execution_options(synchronize_session="fetch")
            )
            await session.commit()
            return result.rowcount > 0
        except SQLAlchemyError as e:
            await session.rollback()
            raise e

    async def delete_one(self, session: AsyncSession, id: int) -> bool:
        obj = await self.get_by_id(session, id)

        if not obj:
            return False
        try:
            await session.delete(obj)
            await session.commit()
            return True
        except SQLAlchemyError:
            await session.rollback()
            return False

    async def delete_many(self, session: AsyncSession, ids: list[int], *conditions) -> bool:
        if not ids:
            return True

        try:
            result: CursorResult = await session.execute(
                sql_delete(self.model)
                .where(self.model.id.in_(ids))
                .where(*conditions)
                .execution_options(synchronize_session="fetch")
            )
            return result.rowcount() > 0
        except SQLAlchemyError:
            await session.rollback()
            return False
