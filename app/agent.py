import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import importlib.util
init_path = os.path.join(project_root, "__init__.py")
spec = importlib.util.spec_from_file_location("root_pkg", init_path)
root_pkg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(root_pkg)

root_agent = root_pkg.root_agent
app = root_pkg.app
cymbal_policy_retriever = getattr(root_pkg, "cymbal_policy_retriever", None)
