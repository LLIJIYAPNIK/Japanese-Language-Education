import os

import aiofiles
import aiohttp
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import UnsplashImages
from backend.services.crud import CRUDBase


class UnsplashService:
    def __init__(
            self,
            api_key: str,
            regular_dir: str,
            small_dir: str,
            db_session: AsyncSession,
            http_client: aiohttp.ClientSession,
            page: int = 1,
            image_number: int = 1
    ):
        self.api_key = api_key
        self.db_session = db_session
        self.http_client = http_client
        self.page = page
        self.image_number = image_number
        self.regular_dir = regular_dir
        self.small_dir = small_dir
        self._unsplash_crud = CRUDBase[UnsplashImages](UnsplashImages)

    async def get_image_data(self) -> tuple[str, str, str]:
        data = await self._get_response()
        image = data["results"][self.image_number]
        return data["results"][self.image_number]["id"], image["urls"]["regular"], image["urls"]["small"]

    async def save_images(self, image_id: str, regular_url: str, small_url: str):
        await self._add_image_to_db(image_id=image_id, image_regular_url=regular_url, image_small_url=small_url)
        await self._download_image(regular_url, self.regular_dir, image_id)
        await self._download_image(small_url, self.small_dir, image_id)

    async def _get_response(self) -> dict | None:
        async with self.http_client.get(
                "https://api.unsplash.com/search/photos",
                params={"query": "Japan", "page": self.page},
                headers={"Authorization": f"Client-ID {self.api_key}"}
        ) as response:
            response.raise_for_status()
            return await response.json()

    async def _is_image_in_db(self, image_id) -> bool:
        result = await self._unsplash_crud.find_one(self.db_session, UnsplashImages.image_id == image_id)

        if result is None:
            return False
        return True

    async def _add_image_to_db(self, image_id: str, image_regular_url: str, image_small_url: str):
        try:
            if not await self._is_image_in_db(image_id):
                await self._unsplash_crud.create(
                    self.db_session,
                    image_id=image_id,
                    image_regular_url=image_regular_url,
                    image_small_url=image_small_url
                )
                await self.db_session.commit()
        except Exception as e:
            await self.db_session.rollback()
            raise e

    async def _download_image(self, url: str, path: str, image_id: str):
        try:
            if not f"{image_id}.jpeg" in os.listdir(path):
                async with self.http_client.get(url) as resp:
                    if resp.status == 200:
                        async with aiofiles.open(f"{os.path.join(path, image_id)}.jpeg", mode='wb') as f:
                            await f.write(await resp.read())
        except Exception as e:
            raise e
