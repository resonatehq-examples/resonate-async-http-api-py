# Resonate Async HTTP API

A simple FastAPI project demonstrating durable, fault-tolerant request processing with Resonate. This project shows how to create an async API that can survive process restarts and handle long-running operations reliably.

## Use Case

This template demonstrates the async request/response pattern with durable execution, perfect for any API that needs to process requests that might take time and must complete reliably even if your server restarts.

## Installation & Usage

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd resonate-async-http-api-py
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Run the server**
   ```bash
   uv run uvicorn main:app --reload
   ```

4. **Test the API**
   ```bash
   # Start a new durable execution (with your own ID for deduplication)
   curl -X POST "http://127.0.0.1:8000/begin?id=your-unique-id" \
     -H "Content-Type: application/json" \
     -d '{"your": "data"}'

   # Check the result
   curl "http://127.0.0.1:8000/wait?id=your-unique-id"
   ```

## API Endpoints

### POST /begin
Starts a new durable execution with optional custom data and ID.

**Parameters:**
- `data` (body, optional): JSON data to process
- `id` (query, optional): Custom promise ID for deduplication

**Response:**
```json
{
  "promise": "your-unique-id",
  "status": "pending",
  "wait": "/wait?id=your-unique-id"
}
```

### GET /wait
Polls for the result of a durable execution.

**Parameters:**
- `id` (query): The promise ID from `/begin`

**Response - Pending:**
```json
{
  "status": "pending",
  "promise_id": "your-unique-id",
  "message": "Processing in progress"
}
```

**Response - Completed:**
```json
{
  "status": "resolved",
  "promise_id": "your-unique-id",
  "result": {"result": "Processed: your data", "timestamp": 1234567890}
}
```

## Key Features

- **Durable Execution**: Functions complete even if the server restarts
- **Deduplication**: Use custom IDs to prevent duplicate work on retries
- **JSON Serialization**: All data is automatically serialized/deserialized
- **Fault Tolerance**: Built-in retry and recovery mechanisms

## Troubleshooting

If you encounter issues:

1. **Check that the server is running**:
   ```bash
   curl http://127.0.0.1:8000/docs
   ```

2. **Verify your data is JSON serializable** - avoid passing objects, classes, or functions

3. **Use custom IDs for important operations** to enable proper deduplication on retries

---

Built with [Resonate](https://resonatehq.io) - Distributed Async Await
