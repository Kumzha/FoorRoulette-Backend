from fastapi import FastAPI
import schemas
from utils import getRestaurantList
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:3000/roulette",
    "https://food-roulete.vercel.app/",
    "https://food-roulete.vercel.app/*",
    "https://food-roulete.vercel.app/roulette",
    # You can add more origins here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/submitAddress', response_model=list[schemas.Restaurant])
def postaddress(payload: schemas.UserSelection):

    #TODO implement address check and formating

    lat = payload.lat
    lng = payload.lng
    wolt = payload.wolt
    bolt = payload.bolt
    
    print(lat, lng, wolt, bolt)


    restaurants_list = getRestaurantList(lat, lng, wolt, bolt)

    # print(restaurants_list)
    return restaurants_list

@app.get('/test')
def test():
    return "test"