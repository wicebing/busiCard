from django.db import models, transaction
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Table_businessCard(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    background = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    color = models.CharField(max_length=20, default="#0068bd33")

    def __str__(self):
        return self.name

    def clean(self):
        if self.name == "":
            raise ValidationError("Must have name")

    @transaction.atomic
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # You have to prepare the file's deletion before it's actually deleted
        storage, path = self.logo.storage, self.logo.path
        super().delete(*args, **kwargs)
        # the file is deleted after the model is deleted
        storage.delete(path)

class Table_personalLink(models.Model):
    id = models.AutoField(primary_key=True)
    link = models.URLField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    footnote = models.CharField(max_length=500)
    pic = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    click = models.IntegerField(default=0)
    startDate = models.DateField()
    endDate = models.DateField()
    show = models.BooleanField(default=True)
    sequence = models.IntegerField(default=0)

    def __str__(self):
        return self.link
    
class Table_linkIPClick(models.Model):
    id = models.AutoField(primary_key=True)
    link = models.ForeignKey(Table_personalLink, on_delete=models.CASCADE)
    ip = models.CharField(max_length=100)
    clickTime = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=1)

    def __str__(self):
        return self.ip
