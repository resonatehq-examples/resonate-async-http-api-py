# python std
import time, uuid
# fast api
from fastapi import FastAPI, Query, HTTPException
# resonate
from resonate import Resonate, Context

app = FastAPI()

# Initialize Resonate - for production, configure with external store
resonate = Resonate()

# Register your durable functions with @resonate.register
# IMPORTANT: All parameters must be serializable
@resonate.register
def foo(context: Context, data):
    # Add your processing, external API calls, database operations, etc.
    # IMPORTANT: Return values must be serializable
    return {"result": f"Processed: {data}", "timestamp": time.time()}

@app.post("/begin")
def begin(data=None, id=None):
    # IMPORTANT: Provide your own ID for deduplication and retries
    # Without a client-provided ID, retries will create duplicate work
    if id is None:
        id = str(uuid.uuid4())

    # Set reasonable defaults for your use case
    if data is None:
        data = {"foo": "bar"}

    # This starts durable execution - the function will complete even if this process dies
    handle = resonate.begin_rpc(func=foo, id=id, data=data)

    return {
        "promise": handle.id,
        "status": "pending",
        "wait": f"/wait?id={handle.id}"
    }

@app.get("/wait")
def wait(id: str):
    try:
        # Retrieve the execution handle by promise ID
        handle = resonate.get(id)

        # Check completion status - handle.done() is non-blocking
        if handle.done():
            result = handle.result()
            return {
                "status": "resolved",
                "promise_id": id,
                "result": result
            }
        else:
            # Still processing - client should poll again
            return {
                "status": "pending",
                "promise_id": id,
                "message": "Processing in progress"
            }
    except Exception as e:
        # Promise not found or execution failed
        raise HTTPException(status_code=404, detail=f"{id} not found")
