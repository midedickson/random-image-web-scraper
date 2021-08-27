from huey.contrib.djhuey import db_task
from scraper.models import Ad
from django.shortcuts import render
from googlesearch import search
from rest_framework.decorators import api_view
import json
import re
from pathlib import Path
import requests
import bs4
from rest_framework.response import Response


@db_task
def scrape_fb_ad(html, adId: Ad):
    try:
        Ad.objects.get(ad_id=adId)
        pass
    except Ad.DoesNotExist:
        soup = bs4.BeautifulSoup(html, 'html.parser')
        script = soup.findAll("script")
        # print(script[8])
        data = str(script[8])[110:-100]
        json_obj = json.loads(data)
        ad_body = json_obj['markup'][0][1]['__html']
        ad_data = json_obj['require'][15][3][0]['props']['adCard']['snapshot']
        Ad.objects.create(ad_id=adId, ad_info=ad_data, ad_body=ad_body)
