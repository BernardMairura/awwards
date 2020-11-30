from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MaxValueValidator,MinValueValidator
from django.utils.text import slugify


# Create your models here.

class UserProfile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    user_image=models.URLField(blank=True,null=True,default="https://res.cloudinary.com/mairura/image/upload/w_1000,c_fill,ar_1:1,g_auto,r_max,bo_5px_solid_red,b_rgb:262c35/v1605442723/p3t7keywhkmswljeuu9x.jpg")
    bio=models.TextField(max_length=150,blank=True,null=True)




    


class Project(models.Model):
   title=models.CharField(max_length=25,blank=True, null=True)
   image=models.URLField(max_length=1000, blank=True, null=True)
   body=models.TextField(max_length=300,blank=True, null=True)
   design=models.IntegerField(default=0)
   usability=models.IntegerField(default=0)
   content=models.IntegerField(default=0)
   user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
   slug = models.SlugField(max_length=200,blank=True, null=True)



   def __str__ (self):
       return self.title


   # auto generating the slug
   def _get_unique_slug(self):
       slug = slugify(self.title)
       unique_slug = slug
       num = 1
       while Project.objects.filter(slug=unique_slug).exists():
          unique_slug = '{}-{}'.format(slug, num)
          num += 1
       return unique_slug
        
    # saving the slug
   def save(self, *args, **kwargs):
      if not self.slug:
          self.slug = self._get_unique_slug()
      super().save()
        




class Review(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    design=models.PositiveIntegerField(default=0,validators=[MaxValueValidator(10)])
    usability=models.PositiveIntegerField(default=0,validators=[MaxValueValidator(10)])
    content=models.PositiveIntegerField(default=0,validators=[MaxValueValidator(10)])
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    review = models.TextField(max_length=750,blank=True, null=True)
    review_date=models.DateField(auto_now_add=True)
    rating=models.FloatField(validators=[MinValueValidator(1),MaxValueValidator(10)])

    def __str__(self):
        return self.user.username


