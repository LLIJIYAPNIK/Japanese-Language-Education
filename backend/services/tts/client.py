import os
import hashlib
from voicevox import Client


class VoicevoxTTSClient:
    def __init__(
            self,
            data_directory: str,
            text_for_speach: str,
            voicevox_client: Client,
            speaker_number: int = 1,
    ):
        self.data_directory = data_directory
        self.text_for_speach = text_for_speach
        self.voicevox_client = voicevox_client
        self.speaker_number = speaker_number

    async def get_audio(self):
        if not os.path.exists(self._get_file_path()):
            await self._save_to_file(await self._generate_audio())
        return self._get_audio_from_path()

    async def _generate_audio(self):
        return await self.voicevox_client.create_audio_query(
            text=self.text_for_speach,
            speaker=self.speaker_number
        )

    async def _save_to_file(self, audio_query):
        with open(self._get_file_path(), "wb") as file:
            file.write(await audio_query.synthesis(speaker=self.speaker_number))

    def _generate_audio_hash(self):
        key = f"{self.text_for_speach.strip().lower()}"
        return hashlib.md5(key.encode()).hexdigest()

    def _get_file_path(self):
        return f"{os.path.join(self.data_directory, self._generate_audio_hash())}.wav"

    def _get_audio_from_path(self):
        with open(self._get_file_path(), "rb") as f:
            return f.read()