# encoding: utf-8

import os
import sys
import string
from workflow import Workflow3, web, ICON_WARNING
from workflow.util import utf8ify

SUGGEST_URL = "https://www.pricerunner.com/public/search/suggest/{}"
GITHUB_SLUG = "sniarn/alfred-pricerunner-workflow"


def suggest(query):
    r = web.get(url=SUGGEST_URL.format(os.getenv('COUNTRY')),
                params={'q': query})
    r.raise_for_status()
    return r.json()


def get_stars(product):
    rating = float(product['rating']['averageRating'])
    rounded = int(round(rating))
    return string.replace('☆☆☆☆☆', '☆', '★', maxreplace=rounded)


def add_product_item(product):
    title = utf8ify(product['name'])
    subtitle = '{} {} – {} – {}'.format(
            product['cheapestPrice']['currency'],
            product['cheapestPrice']['amount'],
            utf8ify(product['categoryName']),
            get_stars(product))
    largetext = '{} – {} {}'.format(
        title,
        product['cheapestPrice']['currency'],
        product['cheapestPrice']['amount'])
    wf.add_item(
        title=title,
        subtitle=subtitle,
        arg=product['url'],
        valid=True,
        largetext=largetext)


def add_suggestion_item(suggestion):
    if 'categories' in suggestion:
        for category in suggestion['categories']:
            if category['name'] == 'all':
                title = utf8ify(suggestion['name'])
            else:
                title = '{} → {}'.format(
                    utf8ify(category['name']),
                    utf8ify(suggestion['name']))
            wf.add_item(
                title=title,
                subtitle=suggestion['type'].capitalize(),
                arg=category['url'],
                valid=True,
                largetext=title)
    else:
        title = utf8ify(suggestion['name'])
        wf.add_item(
            title=title,
            subtitle=suggestion['type'].capitalize(),
            arg=suggestion['url'],
            valid=True,
            largetext=title)


def main(wf):
    query = wf.args[0]
    data = suggest(query)
    for product in data['products']:
        add_product_item(product)
    for suggestion in data['suggestions']:
        add_suggestion_item(suggestion)
    wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow3(
        help_url='https://github.com/{}'.format(GITHUB_SLUG))
    if wf.update_available:
        wf.start_update()
    if not os.getenv('COUNTRY'):
        wf.add_item('No country configured', 'Action this item to get help.',
                    arg=wf.help_url, valid=True, icon=ICON_WARNING)
        wf.send_feedback()
        sys.exit(0)
    else:
        sys.exit(wf.run(main))
