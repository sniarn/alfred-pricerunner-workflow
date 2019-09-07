# PriceRunner Workflow for Alfred

An [Alfred][alfred] workflow for querying [PriceRunner][pricerunner]. You need
to purchase the [Alfred Powerpack][alfred-powerpack] to use this workflow.

## Features

* Look up prices as you type.
* Supports several languages and currencies.
* <kbd>⌘</kbd> + <kbd>L</kbd> displays product name and price in large type.

## Usage

Type the keyword `price` into alfred followed by a search string.

![Screenshot](screenshot.png)

## Installing

Download the [latest release][gh-latest-release] and import it into Alfred.

## Configuration

You can change the language (and thereby currency) the workflow uses by
changing the `COUNTRY` workflow variable. Valid values are (as of this
writing):

* `uk` (default)
* `dk`
* `se`

## Thanks

* [PriceRunner][pricerunner]
* [Alfred-Workflow][alfred-workflow]

[alfred]: https://www.alfredapp.com
[alfred-powerpack]: https://www.alfredapp.com/powerpack
[alfred-workflow]: http://www.deanishe.net/alfred-workflow
[pricerunner]: https://www.pricerunner.com
[gh-latest-release]: https://github.com/sniarn/alfred-pricerunner-workflow/releases/latest
