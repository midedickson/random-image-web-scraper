from hashlib import algorithms_available

from requests import api
from scraper.models import Ad
from django.shortcuts import render
from googlesearch import search
from rest_framework.decorators import api_view
import json
import re
from pathlib import Path
import requests
from .tasks import scrape_fb_ad
import bs4
from rest_framework.response import Response
# Create your views here.
DIR = Path(__file__).resolve().parent
newFilePath = Path.joinpath(DIR, "ads_archive.json")


@api_view(["GET"])
def send_random_photos(request):
    mock_data = open(newFilePath, 'r')
    for data in json.load(mock_data)["data"]:
        url = data["ad_snapshot_url"]
        print(url)
        response = requests.get(url)
        scrape_fb_ad(response.text, data["id"])
    mock_data.close()
    return Response({
        "status": 'done'
    }, status=200)


@api_view(["GET"])
def get_all_ads(request):
    allSavedAds = Ad.objects.all()
    data = []
    for ads in allSavedAds:
        data.append(
            {
                "id": ads.ad_id,
                "body": ads.ad_body,
                "info": ads.ad_info
            }
        )
    return Response({"data": data}, status=200)


def search_google(query):
    img_src_list = []
    while len(img_src_list) == 0:
        search_results = search(query=query, tld="com",
                                num=10, pause=6.0, stop=10)
        list = []
        for i in search_results:
            list.append(i)
        print(list)
        print("listlistlistlistlistlistlist")
        for url in list:
            response = requests.get(url)
            soup = bs4.BeautifulSoup(response.text, 'html.parser')
            all_img = soup.findAll("img", alt=re.compile("dog"))
            for img in all_img:
                # AdPhoto.objects.create(photo=img["src"], keywords=query)
                img_src_list.append(img["src"])
    return img_src_list
