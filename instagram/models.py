from django.db import models


class InstagramPhoto(models.Model):
    online = models.BooleanField(default=False)
    pub_date = models.DateField(blank=True)
    instagram_id = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='instagram', blank=True)
    image_crop = models.ImageField(upload_to='instagram/final', blank=True)
    text = models.TextField(blank=True)
    likes = models.IntegerField(blank=True, null=True)
    # tags = models.ManyToManyField(blank=True)
    comments = models.IntegerField(blank=True, null=True)
    link = models.URLField(blank=True)
    type = models.CharField(max_length=10, blank=True)

    def save(self, *args, **kwargs):
        # Opening the uploaded image
        im = Image.open(self.image)

        output = BytesIO()

        # Resize/modify the image
        width, height = im.size  # Get dimensions

        left = (width - 480) / 2
        top = (height - 480) / 2
        right = (width + 480) / 2
        bottom = (height + 480) / 2

        im = im.crop((left, top, right, bottom))

        # after modifications, save it to the output
        im.save(output, format='JPEG', quality=100)
        output.seek(0)

        # change the imagefield value to be the newley modifed image value
        self.image_crop = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.image.name.split('.')[0], 'image/jpeg',
                                        sys.getsizeof(output), None)

        super(InstagramPhoto, self).save()