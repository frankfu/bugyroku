from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
from django.core.urlresolvers import reverse
from django.utils.timezone import now
from django.template.defaultfilters import default

class LinkVoteCountManager(models.Manager):
    def get_queryset(self):
        return super(LinkVoteCountManager, self).get_queryset().annotate(
            votes=Count('vote')).order_by('-rank_score', '-votes')

class Link(models.Model):
    title = models.CharField("Headline", max_length=100)
    cat_values = (("N", "News"),
                  ("S", "Scholarships"),
                  ("J", "Jobs"))
    category = models.CharField(default="N", max_length=2, choices=cat_values)
    submitter = models.ForeignKey(User)
    submitted_on = models.DateTimeField(auto_now_add=True)
    rank_score = models.FloatField(default=0.0)
    url = models.URLField("URL", max_length=250, blank=True)
    description = models.TextField(blank=True)
    
    with_votes = LinkVoteCountManager()
    objects = models.Manager() #default manager

    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("link_detail", kwargs={"pk": str(self.id)})
    
    def set_rank(self):
        # Based on HN ranking algo at http://amix.dk/blog/post/19574
        SECS_IN_HOUR = float(60*60)
        GRAVITY = 1.2
        
        delta = now() - self.submitted_on
        item_hour_age = delta.total_seconds()
        votes = self.votes - 1
        self.rank_score = votes / pow((item_hour_age+2), GRAVITY)
        self.save()

class Vote(models.Model):
    voter = models.ForeignKey(User)
    link = models.ForeignKey(Link)

    def __unicode__(self):
        return "%s upvoted %s" % (self.voter.username, self.link.title)
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    bio = models.TextField(null=True, default="Stuff about me")
        
    def __unicode__(self):
        return "%s's profile" % self.user
    
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)
        
#signal while saving User
from django.db.models.signals import post_save
post_save.connect(create_profile, sender=User)