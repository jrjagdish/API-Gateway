from pydantic import BaseModel

class ProviderKeyCreate(BaseModel):
    provider_name: str
    provider_key: str
