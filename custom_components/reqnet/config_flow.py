import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import ReqnetApi, ReqnetApiError
from .const import CONF_HOST, DOMAIN


class ReqnetConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            host = user_input[CONF_HOST]

            session = async_get_clientsession(self.hass)
            api = ReqnetApi(session, host)

            try:
                await api.async_get_current_work_parameters()
            except ReqnetApiError:
                errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(host)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=f"reQnet {host}",
                    data={CONF_HOST: host},
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST, default="192.168.1.133"): str,
                }
            ),
            errors=errors,
        )