# collective.volto.acumbamail

[![Acumbamail](https://raw.githubusercontent.com/macagua/collective.volto.acumbamail/refs/heads/main/docs/docs/_static/logo.svg)](https://acumbamail.com/)

An integration for the [Acumbamail](https://acumbamail.com/) service with Plone

## Features

- Add a new subscriber to the Acumbamail list.

## Installation

Install `collective.volto.acumbamail` with `pip`:

```shell
pip install collective.volto.acumbamail
```

And to create the Plone site:

```shell
make create-site
```

## Contribute

- [Issue tracker](https://github.com/collective/collective.volto.acumbamail/issues)
- [Source code](https://github.com/collective/collective.volto.acumbamail/)

### Prerequisites ✅

-   An [operating system](https://6.docs.plone.org/install/create-project-cookieplone.html#prerequisites-for-installation) that runs all the requirements mentioned.
-   [uv](https://6.docs.plone.org/install/create-project-cookieplone.html#uv)
-   [Make](https://6.docs.plone.org/install/create-project-cookieplone.html#make)
-   [Git](https://6.docs.plone.org/install/create-project-cookieplone.html#git)
-   [Docker](https://docs.docker.com/get-started/get-docker/) (optional)

### Installation 🔧

1.  Clone this repository, then change your working directory.

    ```shell
    git clone git@github.com:collective/collective.volto.acumbamail.git
    cd collective.volto.acumbamail
    ```

2.  Install this code base.

    ```shell
    make install
    ```


### Add features using `plonecli` or `bobtemplates.plone`

This package provides markers as strings (`<!-- extra stuff goes here -->`) that are compatible with [`plonecli`](https://github.com/plone/plonecli) and [`bobtemplates.plone`](https://github.com/plone/bobtemplates.plone).
These markers act as hooks to add all kinds of subtemplates, including behaviors, control panels, upgrade steps, or other subtemplates from `plonecli`.

To run `plonecli` with configuration to target this package, run the following command.

```shell
make add <template_name>
```

For example, you can add a content type to your package with the following command.

```shell
make add content_type
```

You can add a behavior with the following command.

```shell
make add behavior
```

```{seealso}
You can check the list of available subtemplates in the [`bobtemplates.plone` `README.md` file](https://github.com/plone/bobtemplates.plone/?tab=readme-ov-file#provided-subtemplates).
See also the documentation of [Mockup and Patternslib](https://6.docs.plone.org/classic-ui/mockup.html) for how to build the UI toolkit for Classic UI.
```

## License

The project is licensed under GPLv2.

## Credits and acknowledgements 🙏

Generated using [Cookieplone (0.9.10)](https://github.com/plone/cookieplone) and [cookieplone-templates (eb40854)](https://github.com/plone/cookieplone-templates/commit/eb4085428af6261227bcb086ece110bbe5475d89) on 2025-11-06 19:48:38.313942. A special thanks to all contributors and supporters!
