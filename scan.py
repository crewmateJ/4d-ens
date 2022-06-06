import requests
from bs4 import BeautifulSoup
from time import sleep
from discord_webhook import DiscordWebhook



url = "YOUR_DISCORD_WEBHOOK_URL"
def notify(input):
    # create other conditions here to filter through
    #
    #
    #
    #
    webhook = DiscordWebhook(url=url, 
        content=str(input))
    webhook.execute()


ls = []    
print('Detecting new four digit numbers...')


def detect_new_fourdigit():
    sleep(1)

    url = "https://opensea.io/collection/ens?search[numericTraits][0][name]=Length&search[numericTraits][0][ranges][0][min]=3&search[numericTraits][0][ranges][0][max]=4&search[sortAscending]=false&search[sortBy]=LISTING_DATE&search[toggles][0]=BUY_NOW"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'
    }
    ctr=0
    old_items = []
    while True:
        # retrieve the html
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, "html.parser")

        # sort the html for pouch #s and Ξ price
        listed_i = soup.findAll("div", {"class": "AssetCardFooter--name"})
        listed_p = soup.findAll("div", {"class": "AssetCardFooter--price"})


        listed_prices = []
        listed_items = []
        for b in range(min(len(listed_i), len(listed_p))):
            # sometimes there is an offer
            if 'Best' in listed_p[b].text or '⚠️' in listed_i[b]:
                continue 
            listed_prices.append(listed_p[b].text.strip('⚠️').strip(' ').strip('Price'))
            listed_items.append(listed_i[b].text.strip('.eth').strip('⚠️').strip(' '))

        # for the first loop
        if ctr==0:
            old_items = listed_items
            ctr = 1
            continue

        # if there has been a new listing
        if listed_items != old_items:
            new = []
            for j in range(len(listed_items)):
                price = listed_prices[j]
                id = listed_items[j]

                if not id.isnumeric():
                    continue

                right_length = bool(len(id) in [3, 4])
                cheap = bool(float(price) < 5)
                is_new = bool(id not in old_items)

                # passes all the tests
                if right_length and cheap and is_new:
                    new.append([price, id])

            if len(new) > 0:
                return new

        if ctr%250 == 0:
            for item in listed_items:
                print(item)
            print(ctr)
            print()

        old_items = listed_items
        ctr += 1
        sleep(1.2)


""" MAIN LOOP """
while True:
    try:
        listings = detect_new_fourdigit()
        for listing in listings:
            if listing not in ls:
                print(listing)    
                notify(str(listing))
                ls.append(listing)
    except Exception as e:
        print(e)
