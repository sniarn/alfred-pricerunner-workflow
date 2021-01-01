# encoding: utf-8

import os
import string
import sys

from workflow import Workflow3, web
from workflow.util import utf8ify

SUGGEST_URL = "https://www.pricerunner.com/public/search/suggest/{}"
COUNTRY = os.getenv('COUNTRY').lower() or "uk"
GITHUB_SLUG = "sniarn/alfred-pricerunner-workflow"


def suggest(query):
    r = web.get(url=SUGGEST_URL.format(COUNTRY), params={'q': query})
    r.raise_for_status()
    return r.json()


def get_stars(product):
    rating = float(product['rating']['averageRating'])
    rounded = int(round(rating))
    return string.replace('☆☆☆☆☆', '☆', '★', maxreplace=rounded)


def get_locale():
    # There is a bug in Python that prevents us from easily getting the user's
    # current locale. We use the COUNTRY workflow parameter instead.
    return {
        'dk': 'da_DK',
        'uk': 'en_GB',
        'se': 'sv_SE',
    }[COUNTRY]


def add_product_item(product):
    title = utf8ify(product['name'])
    from babel.numbers import format_currency
    cheapest_price = utf8ify(format_currency(
        float(product['lowestPrice']['amount']),
        product['lowestPrice']['currency'],
        locale=get_locale()))
    subtitle = '{} – {} – {}'.format(
            cheapest_price,
            utf8ify(product['categoryName']),
            get_stars(product))
    largetext = '{} – {}'.format(title, cheapest_price)
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
        libraries=['./lib'],
        update_settings={'github_slug': GITHUB_SLUG},
        help_url='https://github.com/{}'.format(GITHUB_SLUG))
    if wf.update_available:
        wf.start_update()
    else:
        sys.exit(wf.run(main))
