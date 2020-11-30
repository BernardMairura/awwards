from django.test import TestCase

# Create your tests here.
class PostsTestClass(TestCase):
    '''
    Creating test class for user posts
    '''
    def setUp(self):
        self.kiragu = Profile(first_name='Duncan',last_name='kiragu',username='DunK',email='dunkiragu@gmail.com')
        self.kiragu.save()

        self.new_tag=tag(tag='testing')
        self.new_tag.save_tag()

        self.new_post =Posts(caption="testing testing 1,2",profile=self.kiragu)
        self.new_post.save_posts()

        self.new_post.tag.add(self.new_tag)

    def tearDown(self):
        Profile.objects.all().delete()
        tag.objects.all().delete()
        Posts.objects.all().delete()    

    def test_posts(self):
        posts = Posts.posts()
        self.assertTrue(len(posts)>0)