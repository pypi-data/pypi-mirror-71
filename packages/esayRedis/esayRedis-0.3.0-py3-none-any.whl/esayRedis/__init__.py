import asyncio
import fastapi
import pydantic
import aioredis
import uuid


class EsayRedis:
    def __init__(self):
        self.redis_pool = None
    
    async def init_app(
        self,
        app:fastapi.FastAPI=None,
        config:pydantic.BaseSettings=None
    ):

        if config is not None:
            self.config = config
        else:
            self.config = RedisConfig()

        app.state.REDIS = self

        return 0

    async def init(self):
        if self.redis_pool is not None:
            pass
        else:
            self.redis_pool = await aioredis.create_redis_pool(**self.getconfig())
            await self.conTest() 
        # exception handel by redis
        
    async def Redis(self):

        return await self.redis_pool
    async def conTest(self):
        c = await self.Redis()
        value = str(uuid.uuid4())
        r = await c.set('x', value)
        r = await c.get('x', encoding='utf-8')
        assert value == r
        # exception handel by redis
    async def disconnect(self):
        if self.redis_pool is not None:
            self.redis_pool.close()
            await self.redis_pool.wait_closed()
        else:
            pass

        # exception handel by redis
        
        

    def getconfig(self):
        opts = dict(
            address=self.get_redis_address(),
            encoding = 'utf-8',
            timeout = self.config.redis_connection_timeout,
            password=self.config.redis_password,
            minsize=self.config.redis_pool_minsize,
            maxsize=self.config.redis_pool_maxsize
        )
        return opts

    def get_redis_address(self) -> str:
            return 'redis://%s:%s/%s' % (
                self.config.redis_host,
                self.config.redis_port,
                self.config.redis_db
            )


class RedisError(Exception):
    pass

class RedisConfig(pydantic.BaseSettings):
    class Config:
        env_prefix = ''
        use_enum_values = True
    redis_host: str = '106.14.9.19'
    redis_port: int = 6379
    redis_password: str = None
    redis_db: int = 4
    redis_connection_timeout: int = 3
    redis_decode_responses=True
    redis_pool_minsize: int = 1
    redis_pool_maxsize: int = 50



esayredis = EsayRedis()











 

