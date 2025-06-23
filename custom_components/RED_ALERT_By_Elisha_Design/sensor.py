from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.sensor import SensorEntity # For RedAlertStatusSensor
from homeassistant.components.binary_sensor import BinarySensorEntity # For YouCanLeaveSensor, EarlyAlertSensor
from homeassistant.const import STATE_ON, STATE_OFF

from .const import DOMAIN # Assuming DOMAIN is correctly defined in const.py

# Define constants for unique IDs and sensor names to avoid magic strings
RED_ALERT_SENSOR_TYPE = "red_alert_status"
YOU_CAN_LEAVE_SENSOR_TYPE = "you_can_leave_status"
EARLY_ALERT_SENSOR_TYPE = "early_alert_status"

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the Red Alert sensors from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    # Use entry.entry_id for unique identifiers for devices and entities
    device_info = {
        "identifiers": {(DOMAIN, entry.entry_id)},
        "name": "Red Alert System", # This will be the name of the device in Home Assistant
        "manufacturer": "Your Integration Name", # Replace with your name/company
        # "model": "Alert System", # Optional
        # "sw_version": "1.0.0", # Optional
    }

    entities = [
        RedAlertStatusSensor(coordinator, entry.entry_id, device_info),
        YouCanLeaveSensor(coordinator, entry.entry_id, device_info),
        EarlyAlertSensor(coordinator, entry.entry_id, device_info),
    ]
    async_add_entities(entities, True)


class RedAlertStatusSensor(CoordinatorEntity, SensorEntity): # Inherit from SensorEntity
    """Representation of a Red Alert Status sensor."""

    _attr_has_entity_name = True # Use this to combine device name and entity name
    _attr_name = "Status" # This will result in "Red Alert System Status"
    _attr_icon = "mdi:bell-alert" # Example icon

    def __init__(self, coordinator, entry_id: str, device_info: dict):
        """Initialize the Red Alert Status sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry_id}_{RED_ALERT_SENSOR_TYPE}"
        self._attr_device_info = device_info

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        if self.coordinator.data:
            if len(self.coordinator.data) > 0:
                return "UNSAFE"
            return "SAFE"
        return "UNKNOWN"

    @property
    def extra_state_attributes(self) -> dict:
        """Return the state attributes."""
        if not self.coordinator.data:
            return {}
        return {
            "alert_count": len(self.coordinator.data),
            "alerts": self.coordinator.data,
        }


class YouCanLeaveSensor(CoordinatorEntity, BinarySensorEntity): # Inherit from BinarySensorEntity
    """Representation of a 'You Can Leave' sensor (binary)."""

    _attr_has_entity_name = True
    _attr_name = "Can Leave" # Will result in "Red Alert System Can Leave"
    _attr_icon = "mdi:run-fast" # Example icon for "can leave"
    # _attr_device_class = "safety" # Optional: specify a device class if applicable

    def __init__(self, coordinator, entry_id: str, device_info: dict):
        """Initialize the You Can Leave sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry_id}_{YOU_CAN_LEAVE_SENSOR_TYPE}"
        self._attr_device_info = device_info

    @property
    def is_on(self) -> bool:
        """Return True if it is safe to leave (binary state is 'on')."""
        if self.coordinator.data:
            for alert in self.coordinator.data:
                msg = alert.get("message", "").lower()
                # Assuming these keywords indicate it's NOT safe to leave
                if "siren" in msg or "unsafe" in msg or "אין לצאת" in msg:
                    return False # Cannot leave (binary sensor is 'off')
        return True # Can leave (binary sensor is 'on')


class EarlyAlertSensor(CoordinatorEntity, BinarySensorEntity): # Inherit from BinarySensorEntity
    """Representation of an Early Alert sensor (binary)."""

    _attr_has_entity_name = True
    _attr_name = "Early Alert" # Will result in "Red Alert System Early Alert"
    _attr_icon = "mdi:alert-circle-outline" # Example icon
    # _attr_device_class = "safety" # Optional

    def __init__(self, coordinator, entry_id: str, device_info: dict):
        """Initialize the Early Alert sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry_id}_{EARLY_ALERT_SENSOR_TYPE}"
        self._attr_device_info = device_info

    @property
    def is_on(self) -> bool:
        """Return True if an early alert is active (binary state is 'on')."""
        if self.coordinator.data:
            for alert in self.coordinator.data:
                if alert.get("typeName", "").lower() == "early alert":
                    return True # Early alert is active (binary sensor is 'on')
        return False # No early alert (binary sensor is 'off')
