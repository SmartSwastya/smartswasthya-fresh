# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
# root/smartswasthya/obvious_mapper.py

from tools.smart_logger import SmartLogger
from tools.obvious_router_registrar import register_all_routes
from registry.model_registry import get_all_model_classes

class ObviousMapper:
    registered_routes = []
    registered_models = []

    @classmethod
    @auto_model
    @auto_route
    @auto_logic
    def run(cls):
        logger = SmartLogger("ObviousMapper")

        logger.log_info("Init", "ObviousMapper.run()", "🧠 Running full mapper sequence...")

        # Register routes
        try:
            routes = register_all_routes()
            cls.registered_routes = routes
            logger.log_success("Route", "register_all_routes", f"✅ Registered {len(routes)} routes")
        except Exception as e:
            logger.log_error("Route", "register_all_routes", f"❌ Failed to register routes: {e}")

        # Register models
        try:
            models = get_all_model_classes()
            cls.registered_models = models
            logger.log_success("Model", "get_all_model_classes", f"✅ Registered {len(models)} models")
        except Exception as e:
            logger.log_error("Model", "get_all_model_classes", f"❌ Failed to register models: {e}")

