from fastapi import Request

async def verify_signature(request: Request, call_next):
    print("verify_signature middleware")
    # Do something before the request is processed
    response = await call_next(request)
    # Do something after the request is processed
    return response