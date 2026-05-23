# =========================================================
# 🔥 SEMANTIC EVENT BUS
# =========================================================

from collections import defaultdict

# =========================================================
# 🔥 EVENT SUBSCRIBERS
# =========================================================

EVENT_SUBSCRIBERS = defaultdict(list)

# =========================================================
# 🔥 EVENT REGISTRATION
# =========================================================

def subscribe_event(

    event_name,
    callback
):

    EVENT_SUBSCRIBERS[
        event_name
    ].append(callback)

# =========================================================
# 🔥 EVENT EMISSION
# =========================================================

def emit_event(

    event_name,
    payload=None
):

    responses = []

    subscribers = EVENT_SUBSCRIBERS.get(
        event_name,
        []
    )

    for callback in subscribers:

        try:

            result = callback(payload)

            responses.append({

                "callback":
                    callback.__name__,

                "success":
                    True,

                "result":
                    result
            })

        except Exception as e:

            responses.append({

                "callback":
                    callback.__name__,

                "success":
                    False,

                "error":
                    str(e)
            })

    return responses

# =========================================================
# 🔥 LIST EVENTS
# =========================================================

def list_registered_events():

    return list(
        EVENT_SUBSCRIBERS.keys()
    )
