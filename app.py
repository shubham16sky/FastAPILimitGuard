#Author Pranit Kumar

#--------------------------#
#--------------------------#

from fastapi import FastAPI,Request,Response
from requestCounter import RequestCounter

#--------------------------#
#--------------------------#


#Set Global Variables
REQ_LIMIT = 2
EXPIRATION_TIME = 60 #IN SECONDS

#--------------------------#
#--------------------------#

#Create object of RequestCounter class and create object of FastAPI class
request_counter = RequestCounter()
app = FastAPI()

#--------------------------#
#--------------------------#


# defining a rate limiter middleware
@app.middleware("http")
async def rate_limiter(request:Request,call_next):
    ip = request.client.host
    request_counter.increment_req_count(ip=ip,expiration_time=EXPIRATION_TIME)
    count,retry_time = request_counter.get_req_count(ip=ip)
    req_left = REQ_LIMIT-int(count)

    #set the req_left in request state
    request.state.req_left = req_left

    if count>REQ_LIMIT:
        return Response(f"You have reached the maximum limit of requests, please try after {retry_time} seconds",
                        status_code=429,
                        headers={"Retry-After":str(retry_time)}

                        )
    
    response = await call_next(request)
    return response

#--------------------------#
#--------------------------#



@app.get("/rateLimiter")
async def rateLimiter(request:Request):
    req_left = getattr(request.state, 'req_left', 0)
    return {"msg":f"Successfull. You have {str(req_left)} requests left within a minute"}


    
    


