#Author Pranit Kumar

#--------------------------#
#--------------------------#


import redis 

#--------------------------#
#--------------------------#



class RequestCounter:
    def __init__(self,redis_host='localhost',redis_port=6379,redis_db=0):
        self.redis = redis.StrictRedis(host=redis_host,port=redis_port,db=redis_db)

    def increment_req_count(self,ip,expiration_time=60):
        key = f"request count for :{ip}"

        key_exists = self.redis.exists(key)

        if key_exists:

            count = self.redis.incr(key)
        else:
            count = self.redis.incr(key)
            self.redis.expire(key,expiration_time)
        return count
    
    def get_req_count(self,ip):
        key = f"request count for :{ip}"
        count = self.redis.get(key)
        ttl = self.redis.ttl(key)
        return (int(count),ttl) if count else (0,0)

#--------------------------#
#--------------------------#

