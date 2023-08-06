# Sphinx awesome sampdirective

![GitHub](https://img.shields.io/github/license/kai687/sphinxawesome-sampdirective?color=blue&style=for-the-badge)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/kai687/sphinxawesome-sampdirective/Run%20unit%20tests?style=for-the-badge)
![PyPI](https://img.shields.io/pypi/v/sphinxawesome-sampdirective?style=for-the-badge)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sphinxawesome-sampdirective?style=for-the-badge)
![Code Style](https://img.shields.io/badge/Code%20Style-Black-000000?style=for-the-badge)

This Sphinx extension provides a new directive `samp` which works much like the
interpreted text role
[samp](https://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html#role-samp).
This extension can be used to markup placeholder variables in code blocks.

## Installation

Install the extension:

```console
pip install sphinxawesome-sampdirective
```

This Sphinx extension should work with Python versions newer than 3.6 and recent Sphinx
releases.

## Configuration

To enable this extension in Sphinx, add it to the list of extensions in the Sphinx
configuration file `conf.py`:

```python
extensions = ["sphinxawesome.sampdirective"]
```

## Use

Include the directive in your documents:

```
.. samp::

   $ echo {USERNAME}
```

`USERNAME` will become an _emphasized_ node. In many outputs, it will be rendered as
_`USERNAME`_. For example, in HTML, the above example will be rendered as:

```HTML
<pre>
    <span class="gp">$</span> echo <em class="var">USERNAME</em>
</pre>
```

You can then control the style of the emphasized element with the `.var` class in CSS.
If the code block begins with a prompt character (`#`, `$`, or `~`), they will be marked
up as well. The style for the prompt character is provided by the `pygments` syntax
highlighting module.

The [Sphinx awesome theme](https://github.com/kai687/sphinxawesome-theme) includes
styling for the `samp` directive by default.

## Caveat

This extension does not provide full syntax highlighting. It is currently not possible
to have code blocks with both markup _and_ syntax highlighting. You have to choose
between the following:

- If you need to render markup, for example links, or bold or italic text, choose the
  `parsed-literal` directive.
- If you just want to highlight a placeholder variable, use the `samp` directive
  provided by this extension.
- If you need full syntax highlighting, use the `code-block` directive.
