from django.db import models
from django.db.models.fields import CharField

from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.blocks import BlockQuoteBlock, RawHTMLBlock
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock


from wagtail.wagtailsearch import index


class BlogIndexPage(Page):
    subheading = CharField(max_length=255)

    content_panels = Page.content_panels + [
        FieldPanel('subheading', classname="full"),
    ]

    @property
    def blogs(self):
        blogs = WeblogPage.objects.live().descendant_of(self)

        blogs = blogs.order_by('-date')

        return blogs

    def get_context(self, request):
        blogs = self.blogs

        context = super(BlogIndexPage, self).get_context(request)
        context['blogs'] = blogs
        context['title'] = self.title
        context['subheading'] = self.subheading
        return context


class WeblogPage(Page):
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('html', RawHTMLBlock()),
        ('block_quote', BlockQuoteBlock()),
        ('embed', EmbedBlock()),
    ])

    subheading = CharField(max_length=255)
    date = models.DateField("Post date")

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.FilterField('date'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('subheading', classname="full"),
        FieldPanel('date'),
        StreamFieldPanel('body', classname="full"),
    ]

    def get_context(self, request):
        context = super(WeblogPage, self).get_context(request)
        context['title'] = self.title
        context['subheading'] = self.subheading
        context['body'] = self.body
        return context