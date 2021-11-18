from django.db import models
import uuid
import os

def get_quote_file(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('uploads/quotes', filename)

def get_proposal_file(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('uploads/proposals', filename)

def save_proposal_file(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('uploads/proposal-pdf', filename)

def get_profile_file(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('uploads/dps', filename)


class ProgangUser(models.Model):
    google_id = models.CharField(max_length=300, null=True, blank=True)
    photoUrl = models.CharField(max_length=500, null=True, blank=True)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    organisation = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    mobile = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    profileImg = models.FileField(upload_to=get_profile_file, null=True, blank=True)
    signupToken = models.TextField(null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.firstName

class Consultation(models.Model):
    consult_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=200, null=True, blank=True)
    mobile = models.CharField(max_length=50, null=True, blank=True)
    consultType = models.CharField(max_length=100, null=True, blank=True)
    slot = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return self.name

class Quotation(models.Model):
    quote_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=100)
    emailOrMobile = models.CharField(max_length=200, null=True, blank=True)
    platform = models.CharField(max_length=100, null=True, blank=True)
    requirements = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    quoteFile = models.FileField(upload_to=get_quote_file, null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.name

class Proposal(models.Model):
    proposal_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=200, null=True, blank=True)
    mobile = models.CharField(max_length=50, null=True, blank=True)
    platform = models.CharField(max_length=100, null=True, blank=True)
    requirements = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    pdfFile = models.FileField(upload_to=save_proposal_file, null=True, blank=True)
    proposalFile = models.FileField(upload_to=get_proposal_file, null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.name
    

class Feedback(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    msg = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return self.name
    