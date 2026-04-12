from collective.volto.acumbamail.restapi.services.subscribe.subscribe import (
    AcumbamailSubscribe,
)
from unittest.mock import Mock
from unittest.mock import patch
from zExceptions import BadRequest

import json
import pytest
import requests
import unittest


class TestAcumbamailSubscribe(unittest.TestCase):
    """Test cases for AcumbamailSubscribe service."""

    def setUp(self):
        """Set up test fixtures."""
        # Create mock context and request
        mock_context = Mock()
        mock_request = Mock()

        # Initialize the service with mocked context and request
        # plone.rest.service.Service has no __init__; Zope sets attributes directly
        self.service = AcumbamailSubscribe.__new__(AcumbamailSubscribe)
        self.service.context = mock_context
        self.service.request = mock_request
        self.service.request.get = Mock()
        self.service.request.body = None

    def test_missing_email_raises_bad_request(self):
        """Test that missing email raises BadRequest."""
        self.service.request.get.return_value = {}
        self.service.request.body = None

        with pytest.raises(BadRequest, match=r"The 'email' field is required."):
            self.service.reply()

    def test_empty_email_raises_bad_request(self):
        """Test that empty email raises BadRequest."""
        self.service.request.get.return_value = {}
        self.service.request.body = json.dumps({"email": ""}).encode("utf-8")

        with pytest.raises(BadRequest, match=r"The 'email' field is required."):
            self.service.reply()

    @patch(
        "collective.volto.acumbamail.restapi.services.subscribe.subscribe.api.portal"
    )
    def test_missing_configuration_returns_error(self, mock_api_portal):
        """Test that missing configuration returns error response."""
        self.service.request.get.return_value = {}
        self.service.request.body = json.dumps({"email": "test@example.com"}).encode(
            "utf-8"
        )

        mock_api_portal.get_registry_record.return_value = None

        result = self.service.reply()

        self.assertEqual(result["status"], "error")
        self.assertIn("configuration incomplete", result["message"])

    @patch(
        "collective.volto.acumbamail.restapi.services.subscribe.subscribe.requests.post"
    )
    @patch(
        "collective.volto.acumbamail.restapi.services.subscribe.subscribe.api.portal"
    )
    def test_successful_subscription(self, mock_api_portal, mock_post):
        """Test successful subscription to Acumbamail."""
        self.service.request.get.return_value = {}
        self.service.request.body = json.dumps({"email": "test@example.com"}).encode(
            "utf-8"
        )

        mock_api_portal.get_registry_record.side_effect = [
            "https://acumbamail.com/api/1",
            "test_api_key",
            "test_list_id",
        ]

        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {"success": True}
        mock_post.return_value = mock_response

        result = self.service.reply()

        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["message"], "Subscription successful")
        mock_post.assert_called_once()

    @patch(
        "collective.volto.acumbamail.restapi.services.subscribe.subscribe.requests.post"
    )
    @patch(
        "collective.volto.acumbamail.restapi.services.subscribe.subscribe.api.portal"
    )
    def test_acumbamail_api_error(self, mock_api_portal, mock_post):
        """Test handling of Acumbamail API error response."""
        self.service.request.get.return_value = {}
        self.service.request.body = json.dumps({"email": "test@example.com"}).encode(
            "utf-8"
        )

        mock_api_portal.get_registry_record.side_effect = [
            "https://acumbamail.com/api/1",
            "test_api_key",
            "test_list_id",
        ]

        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {"success": False, "error": "Invalid email"}
        mock_post.return_value = mock_response

        result = self.service.reply()

        self.assertEqual(result["status"], "error")
        self.assertIn("Acumbamail:", result["message"])

    @patch(
        "collective.volto.acumbamail.restapi.services.subscribe.subscribe.requests.post"
    )
    @patch(
        "collective.volto.acumbamail.restapi.services.subscribe.subscribe.api.portal"
    )
    def test_requests_exception_handling(self, mock_api_portal, mock_post):
        """Test handling of requests exceptions."""
        self.service.request.get.return_value = {}
        self.service.request.body = json.dumps({"email": "test@example.com"}).encode(
            "utf-8"
        )

        mock_api_portal.get_registry_record.side_effect = [
            "https://acumbamail.com/api/1",
            "test_api_key",
            "test_list_id",
        ]
        mock_post.side_effect = requests.exceptions.RequestException(
            "Connection timeout"
        )

        result = self.service.reply()

        self.assertEqual(result["status"], "error")
        self.assertIn("Connection timeout", result["message"])

    def test_json_parsing_from_request_body(self):
        """Test parsing JSON data from request body."""
        email = "test@example.com"
        self.service.request.get.return_value = {}
        self.service.request.body = json.dumps({"email": email}).encode("utf-8")

        with patch(
            "collective.volto.acumbamail.restapi.services.subscribe.subscribe.api.portal"
        ) as mock_api_portal:
            mock_api_portal.get_registry_record.return_value = None

            result = self.service.reply()

            # Should reach configuration check, meaning email was parsed correctly
            self.assertEqual(result["status"], "error")
            self.assertIn("configuration incomplete", result["message"])

    def test_malformed_json_fallback(self):
        """Test fallback when JSON parsing fails."""
        self.service.request.get.return_value = {}
        self.service.request.body = b"invalid json"

        with pytest.raises(BadRequest, match=r"The 'email' field is required."):
            self.service.reply()

    @patch(
        "collective.volto.acumbamail.restapi.services.subscribe.subscribe.api.portal"
    )
    def test_registry_exception_handling(self, mock_api_portal):
        """Test handling of registry access exceptions."""
        self.service.request.get.return_value = {}
        self.service.request.body = json.dumps({"email": "test@example.com"}).encode(
            "utf-8"
        )

        mock_api_portal.get_registry_record.side_effect = Exception("Registry error")

        result = self.service.reply()

        self.assertEqual(result["status"], "error")
        self.assertIn("configuration incomplete", result["message"])

    def test_no_request_body(self):
        """Test handling when request has no body."""
        self.service.request.get.return_value = {}
        self.service.request.body = None

        with pytest.raises(BadRequest, match=r"The 'email' field is required."):
            self.service.reply()
