import async_timeout
import aiohttp

from .const import API_CURRENT_WORK_PARAMETERS


class ReqnetApiError(Exception):
    """reQnet API error."""


class ReqnetApi:
    def __init__(self, session: aiohttp.ClientSession, host: str) -> None:
        self._session = session
        self._host = host.strip().replace("http://", "").replace("https://", "").rstrip("/")

    @property
    def base_url(self) -> str:
        return f"http://{self._host}"

    async def async_get_current_work_parameters(self) -> list:
        url = f"{self.base_url}{API_CURRENT_WORK_PARAMETERS}"

        try:
            async with async_timeout.timeout(10):
                response = await self._session.get(url)
                response.raise_for_status()
                data = await response.json(content_type=None)
        except Exception as err:
            raise ReqnetApiError(f"Cannot fetch data from reQnet: {err}") from err

        if not data.get("CurrentWorkParametersResult"):
            raise ReqnetApiError(data.get("Message", "Unknown reQnet API error"))

        values = data.get("Values")

        if not isinstance(values, list):
            raise ReqnetApiError("Invalid reQnet API response: missing Values list")

        return values