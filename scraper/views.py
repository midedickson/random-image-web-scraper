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
# from .tasks import scrape_fb_ad
import bs4
from rest_framework.response import Response


# Create your views here.
DIR = Path(__file__).resolve().parent
newFilePath = Path.joinpath(DIR, "ads_archive.json")


def scrape_fb_ad(html, adId: Ad):
    # f = open("oo-html.html", 'w')
    # f.write(html)
    # f.close()
    try:
        Ad.objects.get(ad_id=adId)
    except Ad.DoesNotExist:
        soup = bs4.BeautifulSoup(html, 'html.parser')
        script = soup.findAll("script")
        data = str(script[8])[110: -100]
        print(data)
        json_obj = json.loads(data)
        # print(json_obj)
        print(json_obj)
        ad_body = json_obj['markup']
        # [0][1]['__html']
        print("adbody >>>>>>>>>>>>>>>>>>>>>>>>>>>", ad_body)
        ad_data = json_obj['require'][15][3][0]['props']['adCard']['snapshot']
        print("addata >>>>>>>>>>>>>>>>>>>>>>>>>>>", ad_data)
        Ad.objects.create(ad_id=adId, ad_info=ad_data, ad_body=ad_body)


@ api_view(["GET"])
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


@ api_view(["GET"])
def get_all_ads(request):
    allSavedAds = Ad.objects.all()
    data = []
    for ads in allSavedAds:
        data.append(
            {
                "id": ads.ad_id,
                "body": ads.ad_body,
                "info": eval(ads.ad_info)
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
