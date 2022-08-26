from django.shortcuts import render

from .models import Announcement

import markdown
# Create your views here.


def announcement(request):
    menu = 'announcement'
    announcement = Announcement.objects.first()
    announcement.post = markdown.markdown(announcement.post,
                                            extensions=[
                                                'markdown.extensions.extra',
                                                'markdown.extensions.codehilite',
                                                'markdown.extensions.toc',
                                            ])
    return render(request, 'announcement.html', locals())
