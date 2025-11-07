from collective.volto.acumbamail import PACKAGE_NAME

import pytest


class TestSetupUninstall:
    @pytest.fixture(autouse=True)
    def uninstalled(self, installer):
        installer.uninstall_product(PACKAGE_NAME)

    def test_addon_uninstalled(self, installer):
        """Test if collective.volto.acumbamail is uninstalled."""
        assert installer.is_product_installed(PACKAGE_NAME) is False

    def test_browserlayer_not_registered(self, browser_layers):
        """Test that ICollectiveVoltoAcumbamailLayer is not registered."""
        from collective.volto.acumbamail.interfaces import (
            ICollectiveVoltoAcumbamailLayer,
        )

        assert ICollectiveVoltoAcumbamailLayer not in browser_layers
