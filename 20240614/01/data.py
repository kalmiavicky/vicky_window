#匯入模組：匯入 requests 用於 HTTP 請求。/匯入 pydantic 用於資料模型驗證。
import requests
from requests import Response
from pydantic import BaseModel, RootModel, Field, field_validator, ConfigDict

#__download_json 函數：定義了一個函數來從指定的 URL 下載 JSON 資料/使用 requests.get 獲取資料，如果失敗則拋出異常
def __download_json():
    # 定義下載 JSON 資料的函數
    url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"

    try:
        # 嘗試從 URL 獲取資料
        res: Response = requests.get(url)
    except Exception:
        # 如果連線失敗，拋出異常
        raise Exception("連線失敗")
    else:
        # 將獲取的 JSON 資料轉換為字典
        all_data: dict[any] = res.json()
        return all_data

#Info 類別：使用 pydantic 定義資料模型，包含 YouBike 站點的各個屬性。/使用 Field 定義別名，讓 JSON 資料對應到模型屬性。/
class Info(BaseModel):
    # 定義 Info 資料模型
    sna: str
    sarea: str
    mday: str
    ar: str
    act: str
    updateTime: str
    total: int
    rent_bikes: int = Field(alias="available_rent_bikes")
    lat: float = Field(alias="latitude")
    lng: float = Field(alias="longitude")
    retuen_bikes: int = Field(alias="available_return_bikes")

    # 設定模型配置，允許使用別名
    model_config = ConfigDict(
        populate_by_name=True,
    )
    #使用 field_validator 處理站點名稱，將其格式化。
    @field_validator("sna", mode='before')
    @classmethod
    def flex_string(cls, value: str) -> str:
        # 處理站點名稱字段，分割後取最後一部分
        return value.split(sep="_")[-1]

#Youbike_Data 類別：
class Youbike_Data(RootModel):
    # 定義 Youbike_Data 根模型，包含一個 Info 列表
    root: list[Info]

#load_data 函數：
def load_data() -> list[dict]:
    # 載入資料的函數
    all_data: dict[any] = __download_json()
    # 驗證並轉換為 Youbike_Data 模型
    youbike_data: Youbike_Data = Youbike_Data.model_validate(all_data)
    # 將模型資料轉換為字典
    data = youbike_data.model_dump()
    return data
#FilterData 類別：定義靜態方法 get_selected_coordinate，根據站點名稱過濾資料並返回對應的 Info 模型。
class FilterData(object):
    @staticmethod
    def get_selected_coordinate(sna: str, data: list[dict]) -> Info:
        # 過濾資料，根據站點名稱找到匹配的站點資料
        right_list: list[dict] = list(filter(lambda item: True if item['sna'] == sna else False, data))
        # 取出第一個匹配的資料
        data: dict = right_list[0]
        # 將資料轉換為 Info 模型並返回
        return Info.model_validate(data)
