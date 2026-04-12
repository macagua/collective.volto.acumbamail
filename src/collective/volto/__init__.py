# See http://peak.telecommunity.com/DevCenter/setuptools#namespace-packages
try:
    __import__("pkg_resources").declare_namespace(__name__)
except ImportError:
    import sys
    from pkgutil import extend_path

    __path__[:] = extend_path(__path__, __name__)


    def __getattr__(name):
        fullname = f"{__name__}.{name}"
        if fullname in sys.modules:
            return sys.modules[fullname]
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
