from typing import Any
import time

class SimpleCache:
    def __init__(self):
        self.store: dict[str, tuple[Any, float | None]] = {}
        
    def get(self, key: str) -> Any | None:
        value, expire_at = self.store.get(key, (None, None))
        
        if expire_at and expire_at < time.time():
            del self.store[key]
            return None
        
        return value
    
    def set(self, key:str, value: Any, ttl: int | None = None):
        expire_at = time.time() + ttl if ttl else None
        self.store[key] = (value, expire_at)
        
        
cache = SimpleCache()