# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib import admin


class ProjectLinkType(models.Model):
    title = models.CharField(verbose_name=_("Title"), max_length=300, blank=False, null=False)
    description = models.TextField(verbose_name=_("Text"), blank=True, null=True)

    class Meta:
        app_label = "crm"
        verbose_name = _('Project Link Type')
        verbose_name_plural = _('Project Link Type')

    def __str__(self):
        return str(self.id) + " " + str(self.title)


class OptionProjectLinkType(admin.ModelAdmin):
    list_display = ('id',
                    'title',
                    'description')

    fieldsets = (
        (_('ProjectLinkType'), {
            'fields': ('title',
                       'description')
        }),
    )
    save_as = True
