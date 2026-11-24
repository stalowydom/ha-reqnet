from datetime import timedelta
import asyncio
import ipaddress
import logging

import aiohttp

from homeassistant.components import persistent_notification
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import ReqnetApi, ReqnetApiError
from .const import API_CURRENT_WORK_PARAMETERS, CONF_HOST, DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)

# automatic search when the unit gets a new address from DHCP (routers without address reservation, e.g. Starlink)
SEARCH_AFTER_FAILS = 3
SEARCH_TIMEOUT = 2  # s per address
SEARCH_PARALLEL = 48


class ReqnetCoordinator(DataUpdateCoordinator[list]):
    def __init__(self, hass: HomeAssistant, api: ReqnetApi, entry=None) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self.api = api
        self.entry = entry
        self._fails = 0

    async def _is_reqnet(self, session: aiohttp.ClientSession, ip: str) -> bool:
        try:
            async with session.get(f"http://{ip}{API_CURRENT_WORK_PARAMETERS}", timeout=aiohttp.ClientTimeout(total=SEARCH_TIMEOUT)) as r:
                if r.status != 200:
                    return False
                data = await r.json(content_type=None)
                return bool(data.get("CurrentWorkParametersResult")) and isinstance(data.get("Values"), list)
        except Exception:  # noqa: BLE001
            return False

    async def _search(self) -> str | None:
        host = self.api._host  # noqa: SLF001
        try:
            net = ipaddress.ip_network(f"{host}/24", strict=False)
        except ValueError:
            return None
        _LOGGER.warning("reQnet: no answer from %s, searching the network %s", host, net)
        sem = asyncio.Semaphore(SEARCH_PARALLEL)
        found: list[str] = []
        session = self.api._session  # noqa: SLF001

        async def check(ip: str) -> None:
            async with sem:
                if not found and await self._is_reqnet(session, ip):
                    found.append(ip)

        await asyncio.gather(*(check(str(ip)) for ip in net.hosts() if str(ip) != host))
        return found[0] if found else None

    async def _async_update_data(self) -> list:
        try:
            data = await self.api.async_get_current_work_parameters()
            self._fails = 0
            return data
        except ReqnetApiError as err:
            self._fails += 1
            if self._fails >= (1 if self.data is None else SEARCH_AFTER_FAILS):
                self._fails = 0
                new_host = await self._search()
                if new_host:
                    old = self.api._host  # noqa: SLF001
                    _LOGGER.warning("reQnet: unit found at a new address %s (was %s)", new_host, old)
                    self.api._host = new_host  # noqa: SLF001
                    if self.entry is not None:
                        self.hass.config_entries.async_update_entry(
                            self.entry, data={**self.entry.data, CONF_HOST: new_host}, title=f"reQnet {new_host}")
                    persistent_notification.async_create(
                        self.hass, f"Rekuperator reQnet zmienił adres na {new_host}. Integracja połączyła się sama.",
                        title="reQnet: nowy adres", notification_id="reqnet_new_host")
                    try:
                        return await self.api.async_get_current_work_parameters()
                    except ReqnetApiError:
                        pass
            raise UpdateFailed(str(err)) from err
