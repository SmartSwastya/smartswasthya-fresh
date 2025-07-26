# ✅ tools/obvious_router.py

# ---------------------------------------------------
# 🚦 Universal Marker Decorators (safe base layer)
# Used across models, routes, logic, tasks
# No imports allowed here to avoid circular trap
# ---------------------------------------------------

# 🚦 Universal Marker Decorators (Safe Base Layer)

def auto_model(x):
    x._auto_marker = "model"
    return x

def auto_route(x):
    x._auto_marker = "route"
    return x

def auto_logic(x):
    x._auto_marker = "logic"
    return x

def auto_task(x):
    x._auto_marker = "task"
    return x

def auto_function(func):
    return func
