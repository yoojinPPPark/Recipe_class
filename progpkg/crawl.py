#!/usr/bin/python

import requests
from bs4 import BeautifulSoup

def crawl(addSource, subList):
    
    recipes = []

    for page_number in range(1, 11):
        url = "https://www.10000recipe.com/recipe/list.html?q=" + addSource + "&order=reco&page=" + str(page_number)

        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        res = soup.find("ul", "rcp_m_list2")
        titles = res.find_all("div", "common_sp_caption_tit line2")
        links = res.find_all("a", "common_sp_link")

        for title in titles:
            recipes.append({"title" : title.get_text()})

        for i in range(len(links)):
            recipes[i]["link"] = "https://www.10000recipe.com" + links[i]["href"]
            page = requests.get("https://www.10000recipe.com" + links[i]["href"])
            soup = BeautifulSoup(page.content, "html.parser")

            res = soup.find("div", "view_step")

            res = res.find_all("div", "media-body")

            recipe = ""

            for j in res:
                recipe += j.get_text().replace("\n", "")

            recipes[i]["recipe"] = recipe

        for i in recipes:
            for word in subList:
                if word in i["recipe"]:
                    if i in recipes:
                        recipes.remove(i)
        
        if len(recipes) > 9:
            break
    
    return recipes[:10]