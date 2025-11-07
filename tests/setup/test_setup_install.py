from collective.volto.acumbamail import PACKAGE_NAME


class TestSetupInstall:
    def test_addon_installed(self, installer):
        """Test if collective.volto.acumbamail is installed."""
        assert installer.is_product_installed(PACKAGE_NAME) is True

    def test_browserlayer(self, browser_layers):
        """Test that ICollectiveVoltoAcumbamailLayer is registered."""
        from collective.volto.acumbamail.interfaces import (
            ICollectiveVoltoAcumbamailLayer,
        )

        assert ICollectiveVoltoAcumbamailLayer in browser_layers

    def test_latest_version(self, profile_last_version):
        """Test latest version of default profile."""
        assert profile_last_version(f"{PACKAGE_NAME}:default") == "1000"
