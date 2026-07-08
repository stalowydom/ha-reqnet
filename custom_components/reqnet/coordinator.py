from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import ReqnetApi, ReqnetApiError
from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class ReqnetCoordinator(DataUpdateCoordinator[list]):
    def __init__(self, hass: HomeAssistant, api: ReqnetApi) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self.api = api

    async def _async_update_data(self) -> list:
        try:
            return await self.api.async_get_current_work_parameters()
        except ReqnetApiError as err:
            raise UpdateFailed(str(err)) from err