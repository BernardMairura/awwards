from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.validators import MaxValueValidator,MinValueValidator
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
from tinymce.models import HTMLField


# Create your models here.

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True,related_name='profile')
    user_image=models.URLField(blank=True,null=True,default="https://res.cloudinary.com/mairura/image/upload/w_1000,c_fill,ar_1:1,g_auto,r_max,bo_5px_solid_red,b_rgb:262c35/v1605442723/p3t7keywhkmswljeuu9x.jpg")
    bio=HTMLField(max_length=150,blank=True,null=True)
    contact = models.CharField(max_length=10,default=1234567800)


    '''
    Creating user profile and saving
    '''
    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)
     
    @receiver(post_save, sender=User) 
    def save_profile(sender,instance,**kwargs):
        instance.profile.save()  
        
    def save_profile(self):
        self.user

    
    def update_profile_bio(self,new_bio):
        self.profile_bio = new_bio
        self.save()
  
    def update_profile_photo(self,new_photo):
        self.profile_photo = new_photo
        self.save()

    def delete_profile(self):
        self.delete()
    '''
    Query for user profiles [Parameter = ID]
    '''
    @classmethod
    def get_by_id(cls,id):
        profile = UserProfile.objects.get(user = id)
        return profile
    
    @classmethod
    def filter_by_id(cls,id): 
        profile = UserProfile.objects.filter(user = id).first()
        return profile
    
    def __str__(self):
        return self.bio




    


class Project(models.Model):
   title=models.CharField(max_length=25,blank=True, null=True)
   user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
   image=CloudinaryField('image', null=True)
   link=models.URLField(max_length=1000, blank=True, null=True)
   body=models.TextField(max_length=300,blank=True, null=True)
   design=models.IntegerField(default=0)
   usability=models.IntegerField(default=0)
   content=models.IntegerField(default=0)
   slug = models.SlugField(max_length=200,blank=True, null=True)
   date=models.DateField(auto_now=True)



   def __str__ (self):
       return self.title

   '''
   Quering projects and getting data for client
   '''
   @classmethod
   def search_by_projects(cls,search_term):
       projects = cls.objects.filter(title__icontains=search_term)
       print(projects)
       return projects 
    
   @classmethod
   def get_profile_projects(cls,profile):
       projects = Project.objects.filter(profile__pk=profile)
       print(projects)
       return projects
    
    
   def __str__(self):
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


class Comments(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comments = models.TextField(max_length=400)
    pro_id = models.IntegerField(default=0)


class NewsLetterRecipients(models.Model):
    name = models.CharField(max_length = 30)
    email = models.EmailField()





