"""API for Somfy bound to HASS OAuth."""
from asyncio import run_coroutine_threadsafe
from typing import Dict, Union

from pymfy.api import somfy_api

from homeassistant import core, config_entries
from homeassistant.helpers import config_entry_oauth2_flow


class ConfigEntrySomfyApi(somfy_api.SomfyApi):
    """Provide a Somfy API tied into an OAuth2 based config entry."""

    def __init__(
        self,
        hass: core.HomeAssistant,
        config_entry: config_entries.ConfigEntry,
        implementation: config_entry_oauth2_flow.AbstractOAuth2Implementation,
    ):
        """Initialize the Config Entry Somfy API."""
        self.hass = hass
        self.config_entry = config_entry
        self.session = config_entry_oauth2_flow.OAuth2Session(
            hass, config_entry, implementation
        )
        super().__init__(None, None, token=self.session.token)

    def refresh_tokens(self,) -> Dict[str, Union[str, int]]:
        """Refresh and return new Somfy tokens using Home Assistant OAuth2 session."""
        run_coroutine_threadsafe(
            self.session.async_ensure_token_valid(), self.hass.loop
        ).result()

        return self.session.token
