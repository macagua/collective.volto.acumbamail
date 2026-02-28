from collective.volto.acumbamail.interfaces import ISettings
from plone import api
from plone.rest import Service
from zExceptions import BadRequest

import logging
import requests


logger = logging.getLogger("collective.volto.acumbamail")

# Official Acumbamail endpoint: adjust according to documentation (generic example)
ACUMBAMAIL_API_URL = "https://acumbamail.com/api/1/addSubscriber"


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
            raise BadRequest("The 'email' field is required.")

        # Read credentials from the registry
        api_key = None
        list_id = None
        try:
            api_key = api.portal.get_registry_record(
                "api_key", interface=ISettings, default="YOUR_API_KEY"
            )
            list_id = api.portal.get_registry_record(
                "list_id", interface=ISettings, default="YOUR_LIST_ID"
            )
        except Exception:
            logger.warning("No configuration records found in Plone registry")

        if not api_key or not list_id:
            logger.error("API key or list_id not configured in the Plone registry tool")
            return {"status": "error", "message": "Acumbamail configuration incomplete"}

        payload = {
            "auth_token": api_key,
            "list_id": list_id,
            "email": email,
            # "name": name,
        }

        try:
            response = requests.post(ACUMBAMAIL_API_URL, json=payload, timeout=10)
            response.raise_for_status()
            result = response.json()
            # Acumbamail's response may vary; adapt it according to the actual API.
            if isinstance(result, dict) and result.get("success"):
                return {"status": "ok", "message": "Subscription successful"}
            else:
                logger.warning(f"Acumbamail responded with an error: {result}")
                return {"status": "error", "message": f"Acumbamail: {result}"}
        except requests.RequestException as exc:
            logger.exception("Error connecting to Acumbamail")
            return {"status": "error", "message": str(exc)}
