import os
import importlib

module_path = os.path.dirname(os.path.abspath(__file__))
routes = [f for f in os.listdir(module_path) if f.endswith(".py") and f != "__init__.py"]
__all__ = routes
for route in routes:
    importlib.import_module(".{}".format(route[:-3]), __name__)

print(
    "Imported routes: %s" % ", ".join(routes)
    if routes
    else "No routes avaiable in the routes directory."
)
