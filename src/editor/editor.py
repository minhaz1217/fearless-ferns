import marimo

__generated_with = "0.14.16"
app = marimo.App(
    width="medium",
    app_title="Fern Editor",
    layout_file="layouts/editor.grid.json",
)


@app.cell
def _():
    import contextlib
    import sys
    import traceback

    import marimo as mo
    return contextlib, mo, traceback


@app.cell(hide_code=True)
def _():
    DEFAULT_CODE = '''\
    from __future__ import annotations


    def cleanup(text):
        """
        A function that cleans given text, escapes html characters, and replaces html entities like `&gt;`
        """
        return text  # no implementation for now


    def element(tagname):
        """
        A simple helper function for wrapping stuff in html tag

        USAGE: element("h1")("Hello world!")
        """
        return lambda text: "<{0}>{1}</{0}>".format(tagname, cleanup(text))


    h1 = element("h1")


    def helloworld():
        return h1("Hello World!")


    if __name__ == "__main__":
        print(helloworld())

    '''
    return (DEFAULT_CODE,)


@app.cell(hide_code=True)
def _(DEFAULT_CODE, mo, on_change):
    editor = mo.ui.code_editor(
        value=DEFAULT_CODE,
        language="python",
        # theme="dark",
        # min_height=1000,
        # max_height=1000,
        # label="# Python editor",
        on_change=on_change,
    )
    editor
    return (editor,)


@app.cell(hide_code=True)
def _(mo, run):
    run_button = mo.ui.button(
        kind="success",
        tooltip="Run the code",
        on_click=run,
        label="▶️",
        keyboard_shortcut="f5",
    )
    run_button
    return


@app.cell(hide_code=True)
def _(mo):
    description = mo.md(f"""
    ## Fern editor

    Edit the code to edit the output 👉
    """)
    description
    return


@app.cell
def _(DEFAULT_CODE):
    code = DEFAULT_CODE

    def on_change(program):
        global code
        code = program
    return (on_change,)


@app.cell
def _(contextlib, editor, setout, traceback):
    def run(ev): 
        with open('__f.log', 'wt') as f, open('__err.log', 'wt') as err:
            with contextlib.redirect_stdout(f), contextlib.redirect_stderr(err):
                try:
                    scope = {
                        **vars(),
                        '__name__': '__main__',
                    }
                    exec(editor.value, scope, scope)
                except Exception as e:
                    traceback.print_exc(e, file=err)

        with open('__f.log', 'rt') as f, open('__err.log', 'rt') as err:
            setout(f.read())
    return (run,)


@app.cell
def _(mo):
    getout, setout = mo.state('')
    return getout, setout


@app.cell
def _(getout, mo):
    mo.Html(getout()).callout()
    return


if __name__ == "__main__":
    app.run()
