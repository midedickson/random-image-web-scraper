from hashlib import algorithms_available
from scraper.models import AdPhoto
from django.shortcuts import render
from googlesearch import search
from rest_framework.decorators import api_view
import json
import re
from random import randint
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
        img_data = []
        while len(img_data) == 0:
            for img in search_google(query_payload):
                img_data.append(img["src"])
        return Response({
            "data": img_data
        }, status=200)


def search_google(query):
    search_results = search(query=query, tld="com",
                            num=10, pause=6.0, stop=10)
    list = []
    for i in search_results:
        list.append(i)
    print(list)
    print("listlistlistlistlistlistlist")
    response = requests.get(list[randint(0, len(list)-1)])
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    BASE_DIR = Path(__file__).resolve().parent
    filePath = Path.joinpath(BASE_DIR, 'html.html')
    file = open(filePath, 'w+')
    file.write(str(soup))
    all_img = soup.find_all("img", alt=re.compile("dog"))
    for img in all_img:
        AdPhoto.objects.create(photo=img["src"], keywords=query)
    return all_img

    # print(soup)
