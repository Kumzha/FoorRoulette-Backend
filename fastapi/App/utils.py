from bolt_data import getBoltRestaurants
from wolt_data import getWoltRestaurants
import schemas, crud
from sqlalchemy.orm import Session


def formatBoltRating(rating: str) -> str:
    return 

def getRestaurantList(lat: float, lng: float, wolt: bool, bolt: bool) -> list[schemas.Restaurant]:

    bolt_restaurants = []
    wolt_restaurants = []

    if(wolt == True):
        wolt_restaurants = getWoltRestaurants(lat, lng)
        
    if(bolt == True):
        bolt_restaurants = getBoltRestaurants(lat, lng)
    
    # print(type((bolt_restaurants+wolt_restaurants)[0]))
    # print(len(bolt_restaurants))
    # print(len(wolt_restaurants))
    return bolt_restaurants + wolt_restaurants

