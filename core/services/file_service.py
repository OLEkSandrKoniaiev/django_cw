import os
from uuid import uuid1


class FileService:

    @staticmethod
    def upload_user_photo(instance, file: str) -> str:
        ext = file.split('.')[-1]
        return os.path.join('user_photo', f'{uuid1()}.{ext}')
