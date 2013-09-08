from django.db import models
from thumbnailer import thumbnailer2
from post.models import Post
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

# Create your models here.

class fileobject(models.Model):

    def uploadpath(instance, filename):
        return ("uploads/"+str(instance.post.id)+instance.subfolder+filename)


    post = models.ForeignKey(Post)
    subfolder = models.CharField(max_length=256, default="/")
    filename = models.FileField(upload_to=uploadpath)
    filetype = models.CharField(max_length=60, blank=True, null=True)


    def save(self):
        super(fileobject, self).save()

       #self.thumbname = thumbobject() 
       #self.thumbname.fileobject = self
       #self.thumbname.filex = 128
       #self.thumbname.filey = 128
       #self.thumbname.save()

       #thumbnaildata = thumbnailer2.thumbnailify(self, (128,128))
       #
       #if thumbnaildata[0]:
       #    self.thumbname = thumbnaildata[0]
       #    self.filetype = thumbnaildata[1]
       #else:
       #    self.filetype = "norender"
        super(fileobject, self).save()

    def delete(self, *args, **kwargs):
        super(fileobject, self).delete(*args, **kwargs)
        default_storage.delete(self.filename)
        default_storage.delete(self.thumbname)


class thumbobject(models.Model):
    #A pointer to the file this is a thumbnail of.
    fileobject = models.ForeignKey(fileobject)
    #This is the actual thumbnail, stored using django storage, whatever that may be.
    filename = models.FileField(upload_to="thumbs/", blank=True, null=True)
    #What the file type is
    filetype = models.CharField(max_length=60, blank=True, null=True)
    #the size of the file.
    filex = models.PositiveSmallIntegerField()
    filey = models.PositiveSmallIntegerField()
    
    class Meta:
        unique_together = ('filex', 'filey', "fileobject")

    def save(self):
        #try:
##           old thumbnailer
#            thumbnaildata = thumbnailer.thumbnailer.thumbnail(self.filename.path,(128,128), forceupdate=True)
        self.filename, self.filetype = thumbnailer2.thumbnailify(self.fileobject, (self.filex, self.filey))
        #except:
        #    self.filetype = "norender"
        super(thumbobject, self).save()

    def delete(self, *args, **kwargs):
        super(thumbobject, self).delete(*args, **kwargs)
        default_storage.delete(self.filename)


 
