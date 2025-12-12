"""Sensor platform for netznoe_hass."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription

from .entity import NetzNoeEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import NetzNoeDataUpdateCoordinator
    from .data import NetzNoeConfigEntry

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="netznoe_hass",
        name="Energy Consumption",
        icon="mdi:lightning-bolt",
        native_unit_of_measurement="kWh",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: NetzNoeConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        NetzNoeSensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class NetzNoeSensor(NetzNoeEntity, SensorEntity):
    """netznoe_hass Sensor class."""

    def __init__(
        self,
        coordinator: NetzNoeDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self.coordinator.data.get("body")
