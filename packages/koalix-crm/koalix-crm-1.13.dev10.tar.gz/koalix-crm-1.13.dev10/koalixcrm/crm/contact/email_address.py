# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _


class EmailAddress(models.Model):
    email = models.EmailField(max_length=200,
                              verbose_name=_("Email Address"))

    class Meta:
        app_label = "crm"
        verbose_name = _('Email Address')
        verbose_name_plural = _('Email Address')
