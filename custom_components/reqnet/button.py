"""Przyciski sterujące centralą reQnet (lokalne REST API: /API/RunFunction?name=…)."""
from dataclasses import dataclass
import logging

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import ReqnetApiError
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class ReqnetButtonDescription(ButtonEntityDescription):
    function: str = ""


BUTTONS: tuple[ReqnetButtonDescription, ...] = (
    ReqnetButtonDescription(key="turn_on", name="Włącz", icon="mdi:fan", function="TurnOn"),
    ReqnetButtonDescription(key="turn_off", name="Wyłącz (czuwanie)", icon="mdi:fan-off", function="TurnOff"),
    ReqnetButtonDescription(key="airing_on", name="Wietrzenie start", icon="mdi:weather-windy", function="TurnOnAiring"),
    ReqnetButtonDescription(key="airing_off", name="Wietrzenie stop", icon="mdi:weather-windy-variant", function="TurnOffAiring"),
    ReqnetButtonDescription(key="automatic", name="Tryb automatyczny", icon="mdi:fan-auto", function="AutomaticMode"),
)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(ReqnetButton(coordinator, entry, d) for d in BUTTONS)


class ReqnetButton(ButtonEntity):
    entity_description: ReqnetButtonDescription

    def __init__(self, coordinator, entry: ConfigEntry, description: ReqnetButtonDescription) -> None:
        self.coordinator = coordinator
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_btn_{description.key}"
        self._attr_name = description.name
        self._attr_has_entity_name = True
        self._attr_device_info = {"identifiers": {(DOMAIN, entry.entry_id)}, "name": "reQnet", "manufacturer": "reQnet"}

    async def async_press(self) -> None:
        try:
            await self.coordinator.api.async_run_function(self.entity_description.function)
        except ReqnetApiError as err:
            raise HomeAssistantError(str(err)) from err
        await self.coordinator.async_request_refresh()
