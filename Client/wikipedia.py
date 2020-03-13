from bs4 import BeautifulSoup
import requests

class Wikipedia:
    def __init__(self, url):
        super().__init__()
        self.__source = requests.get(url).text
        self.__soup = BeautifulSoup(self.__source, 'lxml')

    def scrap_person(self):
        if self.__check_link():
            table = self.__soup.find("table", { "class": "infobox biography vcard" })
            name = table.find("div", { "class": "fn" }).text
            birthday = table.find("span", { "class": "bday" }).text
            deathday = table.find(text="Died").parent.find_next_siblings()
            deathday = deathday[0].find("span").text
            return name, birthday, deathday

        return None, None, None

    def __check_link(self) -> bool:
        table = self.__soup(text="Wikipedia does not have an article with this exact name.")
        if "Wikipedia does not have an article with this exact name." in table:
            return False

        return True
