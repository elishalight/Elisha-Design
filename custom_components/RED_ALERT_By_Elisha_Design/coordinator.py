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
                    text = await resp.text()
                    if not text:
                        _LOGGER.debug("RED ALERT: Empty response from alerts API, no alerts currently.")
                        return []

                    try:
                        data = await resp.json()
                    except Exception:
                        _LOGGER.warning(f"RED ALERT: Failed to parse JSON from alerts API response: {text}")
                        return []

                    if not data:
                        _LOGGER.debug("RED ALERT: Alerts API returned empty data.")
                        return []

                    alerts = data.get("alerts", [])
                    filtered_alerts = []

                    # Filter alerts for the configured city (case insensitive)
                    for alert in alerts:
                        cities = alert.get("cities", [])
                        if any(self.city.lower() == city.lower() for city in cities):
                            filtered_alerts.append(alert)

                    return filtered_alerts

        except Exception as e:
            raise UpdateFailed(f"RED ALERT: Error updating alerts: {e}")
