import logging
from datetime import timedelta
import async_timeout
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import OREF_ALERTS_URL

_LOGGER = logging.getLogger(__name__)

class RedAlertDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, city):
        self.city = city
        self.session = async_get_clientsession(hass)
        super().__init__(
            hass,
            _LOGGER,
            name="RED ALERT data coordinator",
            update_interval=timedelta(minutes=5),
        )

    async def _async_update_data(self):
        try:
            async with async_timeout.timeout(10):
                async with self.session.get(OREF_ALERTS_URL) as resp:
                    if resp.status != 200:
                        raise UpdateFailed(f"Error fetching alerts: {resp.status}")
                    data = await resp.json()
                    # Filter alerts for the city
                    filtered_alerts = []
                    for alert in data.get("alerts", []):
                        cities = alert.get("cities", [])
                        # City names in the JSON may have different formats; compare case-insensitive
                        if any(self.city.lower() in city.lower() for city in cities):
                            filtered_alerts.append(alert)
                    return filtered_alerts
        except Exception as e:
            raise UpdateFailed(f"Error updating alerts: {e}")
