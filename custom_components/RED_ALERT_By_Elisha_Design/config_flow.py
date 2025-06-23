import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, LICENSES_URL

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema({
    vol.Required("license"): str,
    vol.Required("city"): str,
})


class RedAlertConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self):
        self.license = None
        self.city = None

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            license_input = user_input["license"].strip()
            city_input = user_input["city"].strip()

            valid = await self._validate_license(license_input)
            if not valid:
                errors["license"] = "invalid_license"
            else:
                self.license = license_input
                self.city = city_input
                return self.async_create_entry(
                    title=f"RED ALERT: {self.city}",
                    data={"license": license_input, "city": city_input},
                )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )

    async def _validate_license(self, license_key: str) -> bool:
        """Check license against GitHub raw license file."""
        session = async_get_clientsession(self.hass)
        try:
            async with session.get(LICENSES_URL) as resp:
                if resp.status != 200:
                    _LOGGER.error("Failed to fetch license file from GitHub")
                    return False
                text = await resp.text()
                licenses = [line.strip() for line in text.splitlines() if line.strip()]
                if license_key in licenses:
                    return True
        except Exception as e:
            _LOGGER.error(f"License validation error: {e}")
        return False
