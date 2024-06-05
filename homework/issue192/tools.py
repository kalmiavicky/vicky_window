import requests
from  requests import JSONDecodeError
from pydantic import BaseModel,RootModel,Field,field_validator
class Site(BaseModel):
    site_name:str = Field(alias='sitename')
    county:str
    aqi:int
    status:str
    pm25:float = Field(alias='pm2.5')
    date:str = Field(alias='datacreationdate')

    @field_validator("pm25",mode='before')
    @classmethod
    def abc(cls, value:str)->str:
        if value=="":
            return "0.0"
        else:
            return value


class Records(RootModel):
    root:list[Site]

def download_json()->dict[any]:
    aqi_url = 'https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json'
    try:
        response = requests.get(aqi_url)
    except Exception:
        raise Exception("連線失敗")
    else:
        if response.status_code == 200:
            try:
                all_data:dict[any] = response.json()
                return all_data
            except JSONDecodeError:
                raise Exception("api_key為測試用,連線已至上限,請稍後再試")
        else:
            raise Exception("下載狀態碼不是200")
        

def get_data(all_data:dict[any])->list[dict]:
    records:Records = Records.model_validate(all_data['records'])
    data:list[dict] = records.model_dump()
    return data