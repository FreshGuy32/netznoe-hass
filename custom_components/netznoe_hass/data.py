"""Custom types for netznoe_hass."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import NetzNoeApiClient
    from .coordinator import NetzNoeDataUpdateCoordinator


type NetzNoeConfigEntry = ConfigEntry[NetzNoeData]


@dataclass
class NetzNoeData:
    """Data for the Blueprint integration."""

    client: NetzNoeApiClient
    coordinator: NetzNoeDataUpdateCoordinator
    integration: Integration
