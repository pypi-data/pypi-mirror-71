#!/usr/bin/python
# -*- coding: utf-8 -*-

from .Control import *


class Text(Control):

    """Control class wrapper for Text Controls"""

    def __init__(self, Type):
        Control.__init__(self, Type)

    @property
    def Text(self):
        return self.send('innerText;', True).replace('<br>', '  ')

    @Text.setter
    def Text(self, html):
        self.send('innerHTML="' + self.text_encoder(html) + '";')

    def text_encoder(self, text):
        s = text.split('"')
        t = ''
        sl = True
        for i in s:
            if sl:
                t += i
                t += '<q>'
                sl = False
            else:
                t += i
                t += '</q>'
                sl = True
        t = t[:-3]
        t = t.replace('"', '').replace('\n', '<br>').replace('\r', '')
        return t


class Heading(Text):

    """Control for Headings"""

    def __init__(self, Size):
        Text.__init__(self, 'h'+str(Size))


# Heading Sizes

class h1(Heading):

    def __init__(self):
        Heading.__init__(self, 1)


class h2(Heading):

    def __init__(self):
        Heading.__init__(self, 2)


class h3(Heading):

    def __init__(self):
        Heading.__init__(self, 3)


class h4(Heading):

    def __init__(self):
        Heading.__init__(self, 4)


class h5(Heading):

    def __init__(self):
        Heading.__init__(self, 5)


class h6(Heading):

    def __init__(self):
        Heading.__init__(self, 6)


class Paragraph(Text):

    """Control for Pharagraphs"""

    def __init__(self):
        Text.__init__(self, 'p')


class p(Paragraph):

    """Paragraph class wrapper"""


class Anchor(Text):

    """Anchor Element"""

    def __init__(self):
        Text.__init__(self, 'a')

    @property
    def href(self):
        return self.send('href;', True)

    @href.setter
    def href(self, link):
        """The link's destination is specified in the href"""

        self.send('href="' + link + '";')


class a(Anchor):

    """class for a tag"""


class Link(Anchor):

    """class for Link Control"""


class Image(Control):

    def __init__(self):
        self.src = None
        Control.__init__(self, 'img')

    @property
    def alt(self, text):
        self.send('alt;', True)

    @alt.setter
    def alt(self, text):
        self.send('alt="' + text + '";')

    @property
    def AlternativeText(self):
        return self.alt

    @AlternativeText.setter
    def AlternativeText(self, text):
        self.alt = text

    @property
    def src(self, src):
        self.send('src;', True)

    @src.setter
    def src(
        self,
        src,
        name='',
        app=None,
        ):
        if name == '':
            self.send('src="' + src + '";')
        else:
            self.src = src
            app.Register('/images/' + name, self.handler)

    @property
    def Source(self):
        return self.src

    @Source.setter
    def Source(self, src):
        self.src = src

    def handler(self, s):
        s.send_response(200)
        s.send_no_cache_headers()
        s.end_headers()
        s.wfile.write(self.src)


class img(Image):

    pass


class Button(Text):

    def __init__(self):
        Text.__init__(self, 'button')


class button(Button):

    pass


class List(Control):

    def __init__(self, ordered=False):
        if ordered:
            Control.__init__(self, 'ol')
        else:
            Control.__init__(self, 'ul')


def AddItem(self, node):
    self.appendChild(node)


class UnorderedList(List):

    pass


class OrderedList(List):

    def __init__(self):
        List.__init__(self, True)


class ul(UnorderedList):

    pass


class ol(OrderedList):

    pass


class li(Text):

    def __init__(self):
        Text.__init__(self, 'li')


class TextNode(Control):

    def __init__(self, Text):
        self.script_manager = None
        self._hosted = False  # Is added to Form
        self._script = ''  # Javascript code(Used before added to Form)
        self.TagName = TagName  # Tagname of Control = Control type
        self.Id = ''  # Used By Form to identify control Dont change
        self._script += 'var Control = document.createTextNode("'
        +self.Text + '");'
        self.events = []
        self.event_handlers = []


class pre(Control):

    def __init__(self):
        Control.__init__(self, 'pre')

    @property
    def Text(self):
        return self.send('innerHTML;', True)

    @Text.setter
    def Text(self, html):
        self.send('innerHTML="' + html + '";')


class b(Text):

    def __init__(self):
        Text.__init__(self, 'b')


class Bold(b):

    pass


class strong(Text):

    def __init__(self):
        Text.__init__(self, 'strong')


class Important(strong):

    pass


class i(Text):

    def __init__(self):
        Text.__init__(self, 'i')


class Italic(i):

    pass


class em(Text):

    def __init__(self):
        Text.__init__(self, 'em')


class Emphasized(em):

    pass


class mark(Text):

    def __init__(self):
        Text.__init__(self, 'mark')


class Marked(mark):

    pass


class small(Text):

    def __init__(self):
        Text.__init__(self, 'small')


class Small(small):

    pass


class Del(Text):

    def __init__(self):
        Text.__init__(self, 'del')


class Deleted(Del):

    pass


class ins(Text):

    def __init__(self):
        Text.__init__(self, 'ins')


class Inserted(ins):

    pass


class sub(Text):

    def __init__(self):
        Text.__init__(self, 'sub')


class Subscript(sub):

    pass


class sup(Text):

    def __init__(self):
        Text.__init__(self, 'sup')


class Superscript(sup):

    pass


class div(Control):

    def __init__(self):
        Control.__init__(self, 'div')
