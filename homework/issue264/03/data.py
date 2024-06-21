import requests
from requests import Response
from pydantic import BaseModel, Field
import webbrowser

API_KEY = 'AIzaSyBzMGENbUBC-nKRTkKz78WVATWTCoEf9Mk'  # 請替換為您的Google Maps API Key

# 定義下載 Google 地圖美食搜尋資料的函數
def __download_json(query):
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={API_KEY}"
    
    try:
        res: Response = requests.get(url)
    except Exception:
        raise Exception("連線失敗")
    else:
        all_data: dict = res.json()
        return all_data

# 定義 Place 資料模型
class Place(BaseModel):
    name: str
    formatted_address: str
    rating: float
    user_ratings_total: int
    place_id: str

# 載入資料的函數
def load_data(query: str) -> list[dict]:
    all_data: dict = __download_json(query)
    places_data = [Place(**place) for place in all_data['results']]
    return [place.dict() for place in places_data]

# 搜尋並在 Google 地圖上打開結果
def search_and_open(address: str, place_id: str):
    query_url = f"https://www.google.com/maps/search/?api=1&query={address}&query_place_id={place_id}"
    webbrowser.open(query_url)


