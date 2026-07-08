from dataclasses import dataclass

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


@dataclass(frozen=True)
class ReqnetBinarySensorDescription(BinarySensorEntityDescription):
    index: int | None = None
    active_value: int = 1


BINARY_SENSORS: tuple[ReqnetBinarySensorDescription, ...] = (
    ReqnetBinarySensorDescription(
        key="status",
        name="Praca",
        index=0,
        device_class=BinarySensorDeviceClass.RUNNING,
    ),
    ReqnetBinarySensorDescription(
        key="error",
        name="Błąd",
        index=40,
        active_value=0,
        device_class=BinarySensorDeviceClass.PROBLEM,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        ReqnetBinarySensor(coordinator, entry, description)
        for description in BINARY_SENSORS
    )


class ReqnetBinarySensor(CoordinatorEntity, BinarySensorEntity):
    entity_description: ReqnetBinarySensorDescription

    def __init__(
        self,
        coordinator,
        entry: ConfigEntry,
        description: ReqnetBinarySensorDescription,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_has_entity_name = True
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "reQnet",
            "manufacturer": "reQnet",
        }

    @property
    def is_on(self) -> bool | None:
        values = self.coordinator.data
        index = self.entity_description.index

        if index is None or not values or index >= len(values):
            return None

        raw_value = values[index]

        if self.entity_description.key == "error":
            return raw_value != 0

        return raw_value == self.entity_description.active_value