from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONCENTRATION_PARTS_PER_MILLION,
    PERCENTAGE,
    UnitOfPower,
    UnitOfPressure,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


WORK_MODE_MAP = {
    1: "Szybkie grzanie",
    2: "Szybkie chłodzenie",
    3: "Urlop",
    4: "Przewietrzanie",
    5: "Oczyszczanie",
    6: "Kominek",
    8: "Ręczny",
    9: "Inteligentny",
    10: "Pomiar wydajności",
}

BYPASS_MAP = {
    0: "Zamknięty ręcznie",
    1: "Otwarty ręcznie",
    2: "Zamknięty automatycznie",
    3: "Otwarty automatycznie",
}


@dataclass(frozen=True)
class ReqnetSensorDescription(SensorEntityDescription):
    index: int | None = None
    value_map: dict[int, str] | None = None


SENSORS: tuple[ReqnetSensorDescription, ...] = (
    ReqnetSensorDescription(
        key="temperature_current",
        name="Temperatura wewnętrzna",
        index=2,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ReqnetSensorDescription(
        key="supply_airflow",
        name="Wydajność nawiewu",
        index=3,
        native_unit_of_measurement="m³/h",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ReqnetSensorDescription(
        key="extract_airflow",
        name="Wydajność wyciągu",
        index=4,
        native_unit_of_measurement="m³/h",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ReqnetSensorDescription(
        key="humidity",
        name="Wilgotność względna",
        index=7,
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.HUMIDITY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ReqnetSensorDescription(
        key="co2",
        name="Stężenie CO₂",
        index=8,
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        device_class=SensorDeviceClass.CO2,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ReqnetSensorDescription(
        key="work_mode",
        name="Tryb pracy",
        index=10,
        value_map=WORK_MODE_MAP,
    ),
    ReqnetSensorDescription(
        key="bypass",
        name="Bypass",
        index=39,
        value_map=BYPASS_MAP,
    ),
    ReqnetSensorDescription(
        key="intake_temperature",
        name="Temperatura czerpni",
        index=55,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ReqnetSensorDescription(
        key="exhaust_temperature",
        name="Temperatura wyrzutni",
        index=56,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ReqnetSensorDescription(
        key="supply_temperature",
        name="Temperatura nawiewu",
        index=57,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ReqnetSensorDescription(
        key="extract_temperature",
        name="Temperatura wyciągu",
        index=58,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ReqnetSensorDescription(
        key="supply_resistance",
        name="Opór nawiewu",
        index=63,
        native_unit_of_measurement=UnitOfPressure.PA,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ReqnetSensorDescription(
        key="extract_resistance",
        name="Opór wyciągu",
        index=64,
        native_unit_of_measurement=UnitOfPressure.PA,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ReqnetSensorDescription(
        key="supply_fan_percent",
        name="Wysterowanie wentylatora nawiewu",
        index=65,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ReqnetSensorDescription(
        key="extract_fan_percent",
        name="Wysterowanie wentylatora wyciągu",
        index=66,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ReqnetSensorDescription(
        key="supply_fan_power",
        name="Moc wentylatora nawiewu",
        index=81,
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ReqnetSensorDescription(
        key="extract_fan_power",
        name="Moc wentylatora wyciągu",
        index=82,
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ReqnetSensorDescription(
        key="filter_days_left",
        name="Dni do wymiany filtrów",
        index=83,
        native_unit_of_measurement="dni",
    ),
    ReqnetSensorDescription(
        key="error_code",
        name="Kod błędu",
        index=40,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    ReqnetSensorDescription(
        key="firmware_major",
        name="Firmware major",
        index=90,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    ReqnetSensorDescription(
        key="firmware_build",
        name="Firmware build",
        index=91,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    ReqnetSensorDescription(
        key="wifi_firmware",
        name="Firmware WiFi",
        index=93,
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
        ReqnetSensor(coordinator, entry, description)
        for description in SENSORS
    )


class ReqnetSensor(CoordinatorEntity, SensorEntity):
    entity_description: ReqnetSensorDescription

    def __init__(
        self,
        coordinator,
        entry: ConfigEntry,
        description: ReqnetSensorDescription,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_name = description.name
        self._attr_has_entity_name = True
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "reQnet",
            "manufacturer": "reQnet",
        }

    @property
    def native_value(self) -> Any:
        values = self.coordinator.data
        index = self.entity_description.index

        if index is None or not values or index >= len(values):
            return None

        raw_value = values[index]

        if self.entity_description.value_map is not None:
            return self.entity_description.value_map.get(
                raw_value,
                f"Nieznany ({raw_value})",
            )

        return raw_value