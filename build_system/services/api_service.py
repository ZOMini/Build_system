from functools import lru_cache


class APIService():
    def __init__(self):
        pass

    async def get_obj_by_id(self) -> None:
        return 


@lru_cache()
def get_api_service() -> APIService:
    return APIService()
