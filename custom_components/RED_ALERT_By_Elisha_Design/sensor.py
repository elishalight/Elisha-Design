from homeassistant.helpers.entity import Entity
from homeassistant.const import STATE_ON, STATE_OFF

from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        RedAlertStatusSensor(coordinator),
        YouCanLeaveSensor(coordinator),
        EarlyAlertSensor(coordinator),
    ], True)

class RedAlertStatusSensor(Entity):
    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._attr_name = "RED ALERT"
        self._state = None

    @property
    def name(self):
        return self._attr_name

    @property
    def state(self):
        if self.coordinator.data:
            if len(self.coordinator.data) > 0:
                return "UNSAFE"
            return "SAFE"
        return "UNKNOWN"

    @property
    def extra_state_attributes(self):
        if not self.coordinator.data:
            return {}
        return {
            "alert_count": len(self.coordinator.data),
            "alerts": self.coordinator.data,
        }

    async def async_update(self):
        await self.coordinator.async_request_refresh()

class YouCanLeaveSensor(Entity):
    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._attr_name = "You Can Leave"
        self._state = STATE_ON

    @property
    def name(self):
        return self._attr_name

    @property
    def is_on(self):
        if self.coordinator.data:
            for alert in self.coordinator.data:
                msg = alert.get("message", "").lower()
                if "siren" in msg or "unsafe" in msg or "אין לצאת" in msg:
                    return False
        return True

    async def async_update(self):
        await self.coordinator.async_request_refresh()

class EarlyAlertSensor(Entity):
    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._attr_name = "Early ALERT"
        self._state = STATE_OFF

    @property
    def name(self):
        return self._attr_name

    @property
    def is_on(self):
        if self.coordinator.data:
            for alert in self.coordinator.data:
                if alert.get("typeName", "").lower() == "early alert":
                    return True
        return False

    async def async_update(self):
        await self.coordinator.async_request_refresh()
