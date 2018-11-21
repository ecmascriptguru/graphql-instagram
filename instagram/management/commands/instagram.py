from django.core.management.base import BaseCommand
from instagram.models import InstagramPhoto
import urllib2
import json

from datetime import datetime

# Image Processing
import requests
import tempfile
from django.core import files

from PIL import Image

class Command(BaseCommand):
    help = 'Instagram Feed'

    def handle(self, *args, **options):
        url = 'https://www.instagram.com/hotvocals/?__a=1'
        try:
            instagram_feed = urllib2.urlopen(url)
        except:
            instagram_feed = None
                
        if instagram_feed != None:
            data = instagram_feed.read()
            try:
                js = json.loads(str(data))
            except:
                js = None

            insta_cubes = InstagramPhoto.objects.all()
            for x in range(0, len(insta_cubes)):
                insta_cubes[x].instagram_id = js["data"][x]["id"]
                insta_cubes[x].text = js["data"][x]["caption"]["text"]
                insta_cubes[x].likes = js["data"][x]["likes"]["count"]
                insta_cubes[x].comments = js["data"][x]["comments"]["count"]
                insta_cubes[x].link = js["data"][x]["link"]
                insta_cubes[x].type = js["data"][x]["type"]

                insta_photo = js["data"][x]["images"]["standard_resolution"]["url"]

                # Steam the image from the url
                request = requests.get(insta_photo, stream=True)

                # Get the filename from the url, used for saving later
                file_name = insta_photo.split('/')[-1]

                # Create a temporary file
                lf = tempfile.NamedTemporaryFile()

                # Read the streamed image in sections
                for block in request.iter_content(1024 * 8):

                    # If no more file then stop
                    if not block:
                        break

                    # Write image block to temporary file
                    lf.write(block)

                print "Instagram Photo " + str(x) + " done downloading, preparing to save..."
                # Save the temporary image to the model#
                # This saves the model so be sure that is it valid
                insta_cubes[x].image.save(file_name, files.File(lf))
                print "Instagram Photo " + str(x) + "saved, preparing to download next one..."

            self.stdout.write(self.style.SUCCESS('Feed Updated. You are legal. Yay!'))
        else:
            print "Check your code, you are lazy again!"
