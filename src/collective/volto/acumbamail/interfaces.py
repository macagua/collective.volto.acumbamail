"""Module where all interfaces, events and exceptions live."""

from collective.volto.acumbamail import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import provider
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ICollectiveVoltoAcumbamailLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


@provider(IFormFieldProvider)
class ISettings(model.Schema):
    """Acumbamail connector configuration"""

    model.fieldset(
        "general",
        label=_("General settings"),
        fields=["api_key", "list_id"],
    )

    api_key = schema.TextLine(
        title=_("Acumbamail API Key"),
        description=_("Your personal Acumbamail token (https://acumbamail.com/api/)"),
        required=True,
    )

    list_id = schema.TextLine(
        title=_("Acumbamail List ID"),
        description=_(
            "Numeric identifier of the list where subscribers will be added."
        ),
        required=True,
    )
