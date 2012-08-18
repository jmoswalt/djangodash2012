from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    """docstring for Account"""
    name = models.CharField(max_length=500)
    create_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateTimeField(auto_now=True)


class Client(models.Model):
    """docstring for Client"""
    name = models.CharField(max_length=500)
    create_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateTimeField(auto_now=True)


class Profile(models.Model):
    """docstring for Profile"""
    account = models.ForeignKey('Account')
    user = models.ForeignKey(User)


class Contact(models.Model):
    """docstring for Contact"""
    client = models.ForeignKey('Client')
    message = models.ForeignKey('Message')
    name = models.CharField(max_length=500)
    email = models.EmailField()
    create_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateTimeField(auto_now=True)


class Message(models.Model):
    """docstring for Message"""
    profile = models.ForeignKey('Profile')
    client = models.ForeignKey('Client')
    account = models.ForeignKey('Account')
    message = models.TextField()
    create_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateTimeField(auto_now=True)


class SignupLink(models.Model):
    """docstring for SignupLink"""
    message = models.TextField()
    create_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateTimeField(auto_now=True)
