from fastapi import APIRouter
import pandas as pd
from api import app

from controller.get_data import get_campaign_performance_data
from controller.get_data import get_offer_events_from
from controller.get_data import get_clients_data

router = APIRouter()

@router.get("/clients")
async def get_all_clients():
    print('[LOG] response calling route  - /clients')
    json_clients = get_clients_data()
    return json_clients


@router.get('/campaignperf')
async def get_campaign_perfromance(): 
    print("[LOG] response calling route - /campaignperf");
    return get_campaign_performance_data();


