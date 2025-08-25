
# resonate
import time
from resonate import Context, Resonate
from threading import Event

# Initialize Resonate under worker group - for production, configure with external store
resonate = Resonate().remote(group="worker")

# Register your durable functions with @resonate.register
# IMPORTANT: All parameters must be serializable
@resonate.register
def foo(context: Context, data):
    # Add your processing, external API calls, database operations, etc.
    # IMPORTANT: Return values must be serializable
    print("resolved at worker node")
    return {"result": f"Processed: {data}", "timestamp": time.time()}

if __name__ == "__main__":
    resonate.start()
    Event().wait()
