"""Adds config flow for OWRCare."""
from __future__ import annotations

from typing import Any

import voluptuous as vol
from .owrcare import OWRCare, Device as OWRCareDevice, OWRCareConnectionError

from homeassistant.components import onboarding, zeroconf
from homeassistant.config_entries import ConfigFlow
from homeassistant.const import CONF_HOST, CONF_MAC
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN


class OWRCareFlowHandler(ConfigFlow, domain=DOMAIN):
    """Config flow for OWRCare."""

    VERSION = 1
    discovered_host: str
    discovered_device: OWRCareDevice

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initiated by the user."""
        errors = {}

        if user_input is not None:
            try:
                device = await self._async_get_device(user_input[CONF_HOST])
            except OWRCareConnectionError:
                errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(device.info.mac_addr)
                self._abort_if_unique_id_configured(
                    updates={CONF_HOST: user_input[CONF_HOST]}
                )
                return self.async_create_entry(
                    title=device.info.name,
                    data={ CONF_HOST: user_input[CONF_HOST] },
                )
        else:
            user_input = {}

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_HOST): str}),
            errors=errors or {},
        )

    async def async_step_zeroconf(
        self, discovery_info: zeroconf.ZeroconfServiceInfo
    ) -> FlowResult:
        """Handle zeroconf discovery."""
        # Abort quick if the mac address is provided by discovery info
        if mac := discovery_info.properties.get(CONF_MAC):
            await self.async_set_unique_id(mac)
            self._abort_if_unique_id_configured(
                updates={CONF_HOST: discovery_info.host}
            )

        self.discovered_host = discovery_info.host
        try:
            self.discovered_device = await self._async_get_device(discovery_info.host)
        except OWRCareConnectionError:
            return self.async_abort(reason="cannot_connect")

        await self.async_set_unique_id(self.discovered_device.info.mac_addr)
        self._abort_if_unique_id_configured(updates={CONF_HOST: discovery_info.host})

        self.context.update(
            {
                "title_placeholders": {"name": self.discovered_device.info.name},
                "configuration_url": f"http://{discovery_info.host}",
            }
        )
        return await self.async_step_zeroconf_confirm()

    async def async_step_zeroconf_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initiated by zeroconf."""
        if user_input is not None or not onboarding.async_is_onboarded(self.hass):
            return self.async_create_entry(
                title=self.discovered_device.info.name,
                data={
                    CONF_HOST: self.discovered_host,
                },
            )

        return self.async_show_form(
            step_id="zeroconf_confirm",
            description_placeholders={"name": self.discovered_device.info.name},
        )

    async def _async_get_device(self, host: str) -> OWRCareDevice:
        """Get device information from OWRCare device."""
        session = async_get_clientsession(self.hass)
        owrcare = OWRCare(host, session=session)
        return await owrcare.update()

