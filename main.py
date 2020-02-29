import time
import urllib.request
from bs4 import BeautifulSoup
import json
import telebot


def fineSplit(s):
    outStr = ""
    for i in s:
        outStr += i + " "
    outStr = outStr[:-1]
    return outStr


def curSplit(s):
    outStr = ""
    s = s[-2]
    lens = len(s)
    str_main = s[0:lens - 2]
    str_coin = s[lens - 2:lens]
    outStr = str_main + "." + str_coin
    return outStr


def price_diff(list1, list2):
    diff = []
    for i in range(0, len(list1)):
        try:
            toAppend = float(list2[i]) - float(list1[i])
            toAppend = round(toAppend, 2)
            diff.append(toAppend)
        except:
            pass
    return diff


def true_economy(list1, list2):
    diff = []
    for i in range(0, len(list1)):
        try:
            toAppend = (1 - (float(list1[i]) / float(list2[i]))) * 100
            toAppend = round(toAppend, 2)
            diff.append(toAppend)
        except:
            pass
    return diff


def parse():
    name = []
    oldPrice = []
    price = []
    site = urllib.request.urlopen("https://www.atbmarket.com/hot/akcii/economy/")
    soup = BeautifulSoup(site, 'html.parser')
    for tag in soup.find_all("span", {"class": "promo_info_text"}):
        toAppend = tag.text.split()
        # print(toAppend)
        toAppend = fineSplit(toAppend)
        name.append(toAppend)
    for tag in soup.find_all("span", {"class": "promo_old_price"}):
        toAppend = tag.text.split()
        toAppend = fineSplit(toAppend)
        oldPrice.append(toAppend)
    for tag in soup.find_all("div", {"class": "promo_price"}):
        toAppend = tag.text.split()
        toAppend = curSplit(toAppend)
        price.append(toAppend)

    return name, oldPrice, price


def getSale():
    data = {}
    name, oldPrice, price = parse()
    # print(len(price), print(len(oldPrice)), print(len(name)))
    priceDiff = (price_diff(price, oldPrice))
    percentDiff = (true_economy(price, oldPrice))
    for i in range(0, len(priceDiff)):
        data[i] = {}

        data[i]["name"] = str(name[i])
        data[i]["price"] = str(price[i])
        data[i]["old_price"] = str(oldPrice[i])
        data[i]["diff_price"] = str(priceDiff[i])
        data[i]["percentDiff"] = str(percentDiff[i])
    count = len(priceDiff)
    return data, count


if __name__ == '__main__':
    bot = telebot.TeleBot('992798512:AAEv92Bbw02vdB-nnLAVAEDkPzCVbzQWl3M')
    data = getSale()
    print(data)


    @bot.message_handler(commands=['getBest'])
    def getDict(message):
        data, count = getSale()
        print(data)
        for i in range(0, 10):
            toSend = data[i]["name"] + "\nСтарая цена: " + str(data[i]["old_price"]) + " грн\nНовая цена:   " + str(
                data[i]["price"]) + " грн\nЭкономия:     " + str(data[i]["percentDiff"]) + "%, это " + str(
                data[i]["diff_price"]) + " грн"
            bot.send_message(message.chat.id, toSend)


    bot.polling()
# timestr = time.strftime("%Y%m%d-%H%M%S")
# fileName = "dumps/" + timestr + ".json"
# with open(fileName, 'w', encoding='utf-8') as f:
#     json = json.dump(data, f)
