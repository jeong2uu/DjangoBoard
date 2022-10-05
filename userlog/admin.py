# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import User

# Register your models here.
# migrate로 만든 user 모델 등록
admin.site.register(User)
