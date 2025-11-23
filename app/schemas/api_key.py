from pydantic import BaseModel

class Api_key_Response(BaseModel):
    api_key : str
    usage_example : dict
