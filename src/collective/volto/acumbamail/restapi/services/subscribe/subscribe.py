"""Acumbamail subscribe REST API service."""

from collective.volto.acumbamail import _
from collective.volto.acumbamail import logger
from collective.volto.acumbamail.interfaces import ISettings
from plone import api
from plone.restapi.services import Service
from zExceptions import BadRequest

import requests


class AcumbamailSubscribe(Service):
    """REST Service: POST -> /Plone/@acumbamail-subscribe
    This service for subscribing users to Acumbamail mailing list."""

    def reply(self):
        """Subscribe a user to Acumbamail mailing list."""

        # `self.request` already contains the JSON parameters
        try:
            data = self.request.get("BODY", {})
        except Exception:
            data = {}

        # If the data is bytes, decode it and parse as JSON
        import json
        if isinstance(data, bytes):
            data = json.loads(data.decode("utf-8"))

        # If Plone/Volto sends JSON correctly, use request.get_json() alternatively.
        if hasattr(self.request, "body") and self.request.body:
            try:
                import json

                data = json.loads(self.request.body.decode("utf-8"))
            except Exception:
                data = data or {}

        email = data.get("email")
        # name = data.get("name", "")

        if not email:
            raise BadRequest(_("The 'email' field is required."))

        # if not name:
        #     raise BadRequest(_("The 'name' field is required."))

        # Read credentials from the registry
        api_url = None
        api_key = None
        list_id = None
        try:
            api_url = api.portal.get_registry_record(
                "api_url", interface=ISettings, default="YOUR_API_URL"
            )
            if api_url.endswith("/"):
                api_url = api_url[:-1]
            api_key = api.portal.get_registry_record(
                "api_key", interface=ISettings, default="YOUR_API_KEY"
            )
            list_id = api.portal.get_registry_record(
                "list_id", interface=ISettings, default="YOUR_LIST_ID"
            )
        except Exception:
            logger.warning("No configuration records found in Plone registry")

        if not api_url or not api_key or not list_id:
            logger.error(
                "API URL, API key, or list_id not configured in the Plone registry tool"
            )
            return {
                "status": "error",
                "message": _("Acumbamail configuration incomplete"),
            }

        # Construct the API endpoint URL and payload for subscribing the user.
        full_url = f"{api_url}/addSubscriber/?auth_token={api_key}&list_id={list_id}&double_optin=1"  # noqa: E501
        payload = {
            "auth_token": api_key,
            "list_id": list_id,
            "email": email,
            # "name": name,
        }

        try:
            # Note: The actual API endpoint and payload structure may differ based on
            # Acumbamail's API documentation.
            response = requests.post(full_url, json=payload, timeout=10)
            # Check if the request was successful (status code 200-299)
            response.raise_for_status()
            # Parse the response from Acumbamail and determine if the subscription
            # was successful.
            result = response.json()
            # Acumbamail's response may vary; adapt it according to the actual API.
            if isinstance(result, dict) and result.get("success"):
                return {"status": "ok", "message": _("Subscription successful")}
            else:
                logger.warning(f"Acumbamail responded with an error: {result}")
                return {
                    "status": "error",
                    "message": _("Acumbamail: {result}").format(result=result),
                }
        except requests.RequestException as exc:
            logger.exception("Error connecting to Acumbamail")
            return {"status": "error", "message": str(exc)}
