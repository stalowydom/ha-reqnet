from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import ReqnetApi
from .const import CONF_HOST, DOMAIN
from .coordinator import ReqnetCoordinator

PLATFORMS = ["sensor", "binary_sensor", "button"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up reQnet from a config entry."""
    host = entry.data[CONF_HOST]

    session = async_get_clientsession(hass)
    api = ReqnetApi(session, host)
    coordinator = ReqnetCoordinator(hass, api, entry)

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    if not hass.services.has_service(DOMAIN, "run_function"):
        async def _run_function(call) -> None:
            name = call.data["name"]
            params = call.data.get("params") or {}
            for coord in hass.data.get(DOMAIN, {}).values():
                await coord.api.async_run_function(name, **params)
                await coord.async_request_refresh()

        hass.services.async_register(DOMAIN, "run_function", _run_function)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload reQnet config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok