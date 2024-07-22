from django.db import models
from users.models import User

class File(models.Model):
    # FileField to store the uploaded file, with the directory specified as 'uploads/'
    file = models.FileField(upload_to='uploads/')
    
    # ForeignKey to link the file to the user who uploaded it, with cascade delete
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # DateTimeField to store the timestamp of when the file was uploaded, set automatically to now
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # String representation of the File model
    def __str__(self):
        return self.file.name
