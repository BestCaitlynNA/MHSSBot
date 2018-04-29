import asyncio
#import urllib2
import requests

def receive(message):
    return_message = "received message, but no image"
    if (len(message.embeds) > 0):
        embed = message.embeds[0]
        print("url: " + str(embed.image.url))
        return embed.image.url
    if (len(message.attachments) > 0):
        url = message.attachments[0].get('url')
        return_message = "Received message with attachment url " + url
        download_image(url)
    print(return_message)
    return message

def download_image(url):
    print("Downloading image: " + url)
    r = requests.get(url)
    with open('image.png', 'wb') as f:
        f.write(r.content)
    print("Done downloading image: " + url)
