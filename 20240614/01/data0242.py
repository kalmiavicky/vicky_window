import requests
from requests import Response
from pydantic import BaseModel, RootModel, Field,field_validator

def __download_json():
    url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"

    try:
        res:Response = requests.get(url)
    except Exception:
        raise Exception("連線失敗")
    else:
        all_data:dict[any] = res.json()
        return all_data
    

class Info(BaseModel):
    sna:str
    sarea:str
    mday:str
    ar:str
    act:str
    updateTime:str
    total:int
    rent_bikes:int = Field(alias="available_rent_bikes")
    lat:float = Field(alias="latitude")
    lng:float = Field(alias="longitude")
    retuen_bikes:int = Field(alias="available_return_bikes")
    
    #把文字切割 把"sna"的YouBike2.0 用不見
    @field_validator("sna",mode="before")
    @classmethod                                 #類別方法
    def flex_string(cls,value:str)-> str:
        return value.split(sep="_")[-1]
    
class Youbike_Data(RootModel):
    root:list[Info]

def load_data()->list[dict]:
    all_data:dict[any] = __download_json()
    youbike_data:Youbike_Data = Youbike_Data.model_validate(all_data)
    data = youbike_data.model_dump()
    return data



class FilterData(object):
    @staticmethod                    #靜態法
    def get_selected_coordinate(sna:str,data:list[dict]) -> dict:
        # def abc(item:dict)->bool:
        #     if item["sna"] ==sna:
        #         return True
        #     else:
        #         return False
        # right_list:list[dict]=list(filter(abc,data))   # (filter篩選 )搜尋list
        right_list:list[dict]=list(filter(lambda item:True if item["sna"]==sna else False,data)) 
        # return (right_list[0]["lat"],right_list[0]["lng"]) #傳回經緯度
        # return right_list[0]
    
        # print(list(filter(abc,data)))

        # print(sna)
        # print(data)
        return Info(0,0)