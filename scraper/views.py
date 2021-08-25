from hashlib import algorithms_available
from scraper.models import AdPhoto
from django.shortcuts import render
from googlesearch import search
from rest_framework.decorators import api_view
import json
import re
from pathlib import Path
import requests
import bs4
from rest_framework.response import Response
# Create your views here.


@api_view(["POST", "GET"])
def send_random_photos(request):
    if request.method == "GET":
        scrape_fb_ads()
        return Response({
            "data": "img_data"
        }, status=200)


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
            all_img = soup.find_all("img", alt=re.compile("dog"))
            for img in all_img:
                AdPhoto.objects.create(photo=img["src"], keywords=query)
                img_src_list.append(img["src"])
    return img_src_list


def scrape_fb_ads():
    img_src_list = []
    # while len(img_src_list) == 0:
    response = requests.get("https://graph.facebook.com/v11.0/ads_archive?search_terms='money'&ad_reached_countries=['US']&fields=id,ad_creation_time,ad_creative_body,ad_creative_link_caption,ad_creative_link_description,ad_creative_link_title,ad_delivery_start_time,ad_delivery_stop_time,ad_snapshot_url,currency,demographic_distribution,funding_entity,impressions,languages,page_id,page_name,potential_reach,publisher_platforms,spend&limit=100&access_token=EAAN04fZCp9g8BAKCnu2DML2jUH8fh46E4Oz3vKe93A4yeFKhME8zN071d81toxSg8sjRFK2ZAVmv2Mx7lKFY4pLxTzLUYWjCSBE62he832YTYlIZAC5pD9dEVHI6xXR3SFJFtMsZBU3YTs3cgmTycQ2XHUI97WKYfgnyiUM3Vc1f424LbZBirfdczmb1QRDAZD")
    print(response)

    # print(soup)
