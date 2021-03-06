from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.utils.text import slugify
from django.conf import settings
from django.dispatch import receiver
from account_manager.models import Account

# Create your models here.


def upload_location(instance, filename, **kwargs):
    file_path = "book/{author_id}/{title}-{filename}".format(
        author_id=str(instance.author), title=str(instance.title), filename=filename
    )
    return file_path


class EbookPost(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=5000, null=True, blank=True)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True)
    pdf = models.FileField(upload_to=upload_location, null=True, blank=True)
    date_published = models.DateTimeField(
        auto_now_add=True, verbose_name="date published"
    )
    date_updated = models.DateTimeField(auto_now_add=True, verbose_name="date updated")
    author = models.CharField(max_length=50, null=True, blank=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)
    likes = models.ManyToManyField(Account, related_name="users")

    def __str__(self):
        return self.title


@receiver(post_delete, sender=EbookPost)
def submission_delete(sender, instance, **kwargs):
    instance.pdf.delete(False)
    instance.image.delete(False)


def pre_save_ebook_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author + "-" + instance.title)


pre_save.connect(pre_save_ebook_post_receiver, sender=EbookPost)


# python3 manage.py migrate --run-syncdb
