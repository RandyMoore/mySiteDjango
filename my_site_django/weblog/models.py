from django.db import models
from django.db.models.fields import CharField
from django.utils.safestring import mark_safe

from markdown import markdown

from pygments import highlight
from pygments.formatters import get_formatter_by_name
from pygments.lexers import get_lexer_by_name

from wagtail.core import blocks
from wagtail.core.blocks import BlockQuoteBlock, RawHTMLBlock
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index


# Custom blocks for StreamField.  From https://gist.github.com/frankwiles/74a882f16704db9caa27
# See also http://docs.wagtail.io/en/v1.9/releases/1.6.html#render-and-render-basic-methods-on-streamfield-blocks-now-accept-a-context-keyword-argument
class CodeBlock(blocks.StructBlock):
    """
    Code Highlighting Block
    """
    LANGUAGE_CHOICES = (
        ('python', 'Python'),
        ('bash', 'Bash/Shell'),
        ('html', 'HTML'),
        ('css', 'CSS'),
        ('scss', 'SCSS'),
    )

    language = blocks.ChoiceBlock(choices=LANGUAGE_CHOICES)
    code = blocks.TextBlock()

    class Meta:
        icon = 'code'

    def render(self, value, context=None):
        src = value['code'].strip('\n')
        lang = value['language']

        lexer = get_lexer_by_name(lang)
        formatter = get_formatter_by_name(
            'html',
            linenos=None,
            cssclass='codehilite',
            style='default',
            noclasses=False,
        )
        return mark_safe(highlight(src, lexer, formatter))


class MarkDownBlock(blocks.TextBlock):
    """ MarkDown Block """

    class Meta:
        icon = 'code'

    def render_basic(self, value, context=None):
        md = markdown(
            value,
            [
                'markdown.extensions.fenced_code',
                'codehilite',
            ],
        )
        return mark_safe(md)


# Page Models
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
        ('code', CodeBlock()),
        ('markdown', MarkDownBlock()),
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

