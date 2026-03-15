from fastapi import FastAPI, status
from fastapi.requests import Request
import time
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

def register_middleware(app:FastAPI):

    @app.middleware('http')
    async def custom_logging(request:Request, call_next):
        start_time = time.time()
        print("before", start_time)

        response = await call_next(request)
        processing_time = time.time() - start_time
        
        message  = f"{request.client.host}- {request.method} - {request.url.path} - {response.status_code}- completed after {processing_time}"
        print(message)
        return response
    
    # @app.middleware('http')
    # async def authorization(request: Request, call_next):
    #     excluded_paths = ["/api/v1/auth/login", "/api/v1/auth/signup", "/docs", "/redoc", "/openapi.json"]
    #     if request.url.path in excluded_paths:
    #      response = await call_next(request)
    #      return response
    #     if not "Authorization" in request.headers:
    #         return JSONResponse(
    #             content={
    #                 "message": "Not Authenticated",
    #                 "resolution": "Please provide  the right credentials to prceed"
    #             },
    #             status_code=status.HTTP_401_UNAUTHORIZED
    #         )
    #     response = await call_next(request)
    #     return response
    
    app.add_middleware(
                       CORSMiddleware,
                       allow_origins=["*"],
                       allow_methods=["*"],
                       allow_headers=["*"],
                       allow_credentials = True,
     )
    
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts = ["*"]
    )
