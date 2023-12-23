
# FastAPILimitGuard

A simple implementation of a rate limiter for FastAPI applications. This rate limiter helps control the rate of incoming requests per IP address, preventing abuse and ensuring a fair distribution of resources.

## Introduction

FastAPILimitGuard is designed to mitigate abuse and manage resource allocation in FastAPI applications. FastAPILimitGuard allows 2 requests per IP in 60 seconds. This ensures a balanced and controlled flow of incoming requests, preventing potential service degradation.

## Features

- **FastAPI Middleware**: Integrates seamlessly with FastAPI as middleware for handling rate limiting on incoming requests.
- **Adjustable Configuration**: Easily configure the token bucket parameters to suit your application's requirements.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/shubham16sky/FastAPILimitGuard.git
   cd FastAPILimitGuard
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the FastAPI application:

   ```bash
   uvicorn app:app --reload
   ```

## Configuration

Adjust the token bucket parameters in the `RequestCounter` class to customize the rate-limiting behavior. Key parameters include:

- `REQ_LIMIT`: Maximum requests allowed per minute.
- `EXPIRATION_TIME`: Expiration time for the request count in seconds.

```python
# requestCounter.py

class RequestCounter:
    def __init__(self, redis_host='localhost', redis_port=6379, redis_db=0):
        # ... (constructor implementation)

    def increment_req_count(self, ip, expiration_time=60):
        # ... (method implementation)

    def get_req_count(self, ip):
        # ... (method implementation)
```

## Usage

1. Import the `RequestCounter` class and create an instance:

   ```python
   from requestCounter import RequestCounter

   request_counter = RequestCounter()
   ```

2. Add the rate limiter as middleware in your FastAPI application (`app.py`):

   ```python
   from fastapi import FastAPI, Request, Response
   from requestCounter import RequestCounter

   # ... (existing code)

   request_counter = RequestCounter()

   @app.middleware("http")
   async def rate_limiter(request: Request, call_next):
       ip = request.client.host
       request_counter.increment_req_count(ip=ip, expiration_time=EXPIRATION_TIME)
       count, retry_time = request_counter.get_req_count(ip=ip)
       req_left = REQ_LIMIT - int(count)

       # ... (existing middleware code)

   # ... (existing code)
   ```

3. Run your FastAPI application and test the rate limiter:

   ```bash
   uvicorn app:app --reload
   ```

## Example Endpoint

Visit the `/rateLimiter` endpoint to test the rate limiter:

- `GET /rateLimiter`

   ```json
   {"msg": "Successfully. You have {req_left} requests left within a minute"}
   ```

