from bs4 import BeautifulSoup
from bs4.element import Tag
from codecs import open
import requests
import click
import sys
import re
import html2text

_index_selector_m = re.compile('^\[(-{0,1}\d+){0,1}:{0,1}(-{0,1}\d+){0,1}\]$')
_attribute_selector_m = re.compile('^\[([^0-9].+)\]$')
_group_separator_m = re.compile('^and$', re.IGNORECASE)
_html_tag_m = re.compile('^\s*</{0,1}(\w+)')

_html2text = html2text.HTML2Text(bodywidth=0)


def select_elements(parents, selector):
    m = _index_selector_m.match(selector)
    if m:
        if m.group(1):
            start_index = int(m.group(1))
        else:
            start_index = 0

        if m.group(2):
            end_index = int(m.group(2))
        else:
            end_index = start_index + 1
        return parents[start_index: end_index]

    elements = []
    m = _attribute_selector_m.match(selector)
    if m:
        for p in parents:
            elements.append(p[m.group(1)])
        return elements

    for p in parents:
        elements.extend(p.select(selector))
    return elements


def prettify_text(element):
    if isinstance(element, Tag):
        return _html2text.handle(element.prettify())
    else:
        return element


def prettify_html(element):
    if isinstance(element, Tag):
        return element.prettify()
    else:
        return element


def print_element(element, format):
    if format == "markdown-text":
        click.echo(prettify_text(element))
    elif format == "pretty-html":
        click.echo(prettify_html(element))
    else:
        # html
        click.echo(str(element))


@click.command()
@click.option('--pipe', '-P', default=False, is_flag=True, help='pipe mode')
@click.option('--encoding', '-e', default='utf-8', help='page encoding')
@click.option('--separator', '-s', default=None, type=str, help='separator between multi elements, default to empty')
@click.option(
    '--format', '-F',
    default="markdown-text",
    help='print format, available formats are: `markdown-text`, `html`, `pretty-html`, default to `markdown-text`'
)
@click.argument('url')
@click.argument('selectors', nargs=-1)
def parse_page(pipe, format, encoding, separator, url, selectors):
    if pipe:
        content = sys.stdin.read()
        selectors = [url] + list(selectors)
    elif url.startswith('http://') or url.startswith('https://'):
        r = requests.get(url)
        r.encoding = encoding
        content = r.text
    else:
        with open(url, 'r', encoding) as f:
            content = f.read()

    soup = BeautifulSoup(content, 'html5lib')

    if len(selectors) == 0:
        print_element(soup, format)

    selectors_groups = []
    current_group = []
    for selector in selectors:
        if _group_separator_m.match(selector):
            selectors_groups.append(current_group)
            current_group = []
        else:
            current_group.append(selector)
    selectors_groups.append(current_group)

    has_content_before = False
    if separator:
        separator = separator.replace('\\n', '\n')
    for selectors_group in selectors_groups:
        elements = [soup]
        for selector in selectors_group:
            elements = select_elements(elements, selector)

        for e in elements:
            if has_content_before and separator:
                click.echo(separator)
            print_element(e, format)
            has_content_before = True


if __name__ == '__main__':
    parse_page()
