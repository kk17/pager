from bs4 import BeautifulSoup
from bs4.element import Tag
from codecs import open
import requests
import click
import sys
import re

_index_selector_m = re.compile('^\[(-{0,1}\d+){0,1}:{0,1}(-{0,1}\d+){0,1}\]$')
_attribute_selector_m = re.compile('^\[([^0-9].+)\]$')
_group_separator_m = re.compile('^and$', re.IGNORECASE)
_html_tag_m = re.compile('^\s*</{0,1}(\w+)')


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


def prettify(element):
    if isinstance(element, Tag):
        html_text = element.prettify()
        not_tag_lines = []
        for line in html_text.splitlines():
            if not _html_tag_m.match(line):
                not_tag_lines.append(line)
        return '\n'.join(not_tag_lines)
    else:
        return element


@click.command()
@click.option('--pipe', '-P', default=False, is_flag=True, help='pipe mode')
@click.option('--encoding', '-e', default='utf-8', help='page encoding')
@click.option('--blanks', '-b', default=0, type=int, help='separate blank line num')
@click.option('--raw', default=False, is_flag=True, help='return raw html')
@click.argument('url')
@click.argument('selectors', nargs=-1)
def parse_page(pipe, raw, encoding, blanks, url, selectors):
    if pipe:
        content = "\n".join(sys.stdin.readlines())
        selectors = [url] + list(selectors)
    elif url.startswith('http://') or url.startswith('https://'):
        r = requests.get(url)
        r.encoding = encoding
        content = r.text
    else:
        with open(url, 'r', encoding) as f:
            content = f.read()

    selectors_groups = []
    current_group = []
    for selector in selectors:
        if _group_separator_m.match(selector):
            selectors_groups.append(current_group)
            current_group = []
        else:
            current_group.append(selector)
    selectors_groups.append(current_group)

    soup = BeautifulSoup(content, 'html5lib')

    for selectors_group in selectors_groups:
        elements = [soup]
        for selector in selectors_group:
            elements = select_elements(elements, selector)

        for e in elements:
            if not raw:
                click.echo(prettify(e))
            else:
                click.echo(str(e))
            if blanks > 0:
                click.echo('\n' * (blanks - 1))


if __name__ == '__main__':
    parse_page()
