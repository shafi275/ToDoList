from django.db import models
from django.contrib.auth.models import User
class Task(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    tasktitle = models.CharField(max_length=30)
    taskdesc = models.TextField()
   
    time = models.DateTimeField(auto_now_add=True)
          
    def __str__(self):
        return self.tasktitle
