#!/usr/bin/python
import os
import json
import urllib.request as urllib2
import logging
import epd2in13_V3
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne
import time
import traceback

# Set current directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

epd = epd2in13_V3.EPD()
epd.init()
print(dir(epd))

epd.Clear()
# get api data
def getApi(epd):
    try:
      f = urllib2.urlopen('http://localhost/admin/api.php?summary&auth=76e2939b03cc0303521bf9ed49b11290d7bfeedec0087b1cb47915ab869bbd02')
      json_string = f.read()
      parsed_json = json.loads(json_string)
      adsblocked = parsed_json['ads_blocked_today']
      ratioblocked = float(parsed_json['ads_percentage_today'])
      status = parsed_json['status']
      f.close()

    # Init Screen
      logging.info("init and Clear")
      time.sleep(1)
      
      # Load graphic
      logging.info("Drawing")
      fontF = ImageFont.truetype(FredokaOne, 32)
      fontP = ImageFont.truetype(FredokaOne, 20)
      HBlackimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126
      HRYimage = Image.new('1', (epd.height, epd.width), 255)
      drawry = ImageDraw.Draw(HRYimage)
      draw = ImageDraw.Draw(HBlackimage)
      # img = Image.open("./logoA.jpg")
      # HRYimage.paste(img, (150,20))
      print("adsblocked: ", adsblocked)
      print("ratioblocked: ", ratioblocked)
      print("status: ", status)
      draw.text((20,20), str(adsblocked), font = fontF, fill = 0)
      draw.text((20,50), str("%.1f" % round(ratioblocked,2)) + "%", font = fontF, fill = 0)
      draw.text((120,60), str(status), font = fontP, fill = 0)
      draw.text((120,30), '[ NCMr ]', font = fontP, fill = 0)

      # epd.display(epd.getbuffer(img), epd.getbuffer(HBlackimage))
      epd.displayPartial(epd.getbuffer(HBlackimage))
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd2in13_V3.epdconfig.module_exit()
        exit()

while (True):
    getApi(epd)
    time.sleep(10)
