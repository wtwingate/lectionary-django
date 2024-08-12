# Lectionary

## About

This is the source code for [lectionary2019.com](https://lectionary2019.com), an interactive web app for the Sunday, Holy Day, and Commemoration Lectionary found in the [Book of Common Prayer 2019](https://bcp2019.anglicanchurch.net/).

The purpose of this app is to provide pastors, music directors, and church administrators accurate information and a convenient set of tools for working with the lectionary. Currently, this project is in "open beta" so suggestions, contributions, and bug reports are more than welcome!

## Coming Soon

-   Collect of the Day
-   Readings from the Apocrypha
-   Alternate lesson options
-   Traditional language versions
-   PDF generator

## How to Contribute

### Dependencies

-   Python 3.12
-   Node.js
-   Docker

### The Stack

I've tried to keep everything simple and limit the amount of third-party dependencies. At its core, this is an _almost_ pure vanilla Django app using PostgreSQL. The front-end is styled using [Tailwind CSS](https://tailwindcss.com/), and there's a good chance I'll be integrating [HTMX](https://htmx.org/) once I find a sufficient justification for it.

The formatting and linting of Python code is done with `ruff`. Django templates are formatted and linted with a combination of `prettier` (for ordering the Tailwind CSS classes) and `djlint`. Unfortunately, these two don't play well together. For the most part, you can just stick with using `djlint`.

### Setup

You will need to get your own [ESV API key](https://api.esv.org/) for local development. It's free, and only takes a minute to set up for personal projects.

In your clone of the repository, create a `.env` file with the following contents:

```bash
export DJANGO_SETTINGS_MODULE=website.settings_dev
export ESV_API_KEY=<your key goes here>
```

Next, you will need to run the provided script to set up a Docker container running PostgreSQL:

```
./scripts/database.sh
```

Then, run the script which loads your environment variables and starts up the Django development server:

```
./scripts/server.sh
```

The final step is just to get Tailwind CSS running and watching for changes:

```
npm run watch
```

Now, visit `localhost:8000` in your browser and tinker away!
