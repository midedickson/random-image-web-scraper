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
        return Response({
            "data": "here I am!"
        }, status=200)

    if request.method == "POST":
        query_payload = json.loads(request.body)["query"]
        img_data = search_google(query_payload)
        return Response({
            "data": img_data
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

    # print(soup)
