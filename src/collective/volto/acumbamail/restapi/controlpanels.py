"""Acumbamail REST API controlpanel adapter."""

from collective.volto.acumbamail.interfaces import ISettings
from plone.restapi.controlpanels import RegistryConfigletPanel
from plone.restapi.interfaces import IControlpanelLayer
from zope.component import adapter
from zope.interface import Interface


@adapter(Interface, IControlpanelLayer)
class AcumbamailSettingsControlpanel(RegistryConfigletPanel):
    """REST API controlpanel adapter for Acumbamail settings."""

    schema = ISettings
    schema_prefix = None
    configlet_id = "AcumbamailSettings"
    configlet_category_id = "Products"
