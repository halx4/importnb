
__importnb__ imports notebooks as modules & packages.

[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/deathbeds/importnb/master?urlpath=lab/tree/readme.ipynb)[![Build Status](https://travis-ci.org/deathbeds/importnb.svg?branch=master)](https://travis-ci.org/deathbeds/importnb)[![PyPI version](https://badge.fury.io/py/importnb.svg)](https://badge.fury.io/py/importnb)![PyPI - Python Version](https://img.shields.io/pypi/pyversions/importnb.svg)![PyPI - Format](https://img.shields.io/pypi/format/importnb.svg)![PyPI - Format](https://img.shields.io/pypi/l/importnb.svg)[
![Conda](https://img.shields.io/conda/pn/conda-forge/importnb.svg)](https://anaconda.org/conda-forge/importnb)[
![GitHub tag](https://img.shields.io/github/tag/deathbeds/importnb.svg)](https://github.com/deathbeds/importnb/tree/master/src/importnb)

    pip install importnb
    
---

    conda install -c conda-forge importnb

# `importnb` works in Python and IPython

Use the `Notebook` context manager.

    >>> from importnb import Notebook

### For brevity

[`importnb.loader`](src/notebooks/loader.ipynb) will find notebooks available anywhere along the [`sys.path`](https://docs.python.org/2/library/sys.html#sys.path).


```python
    with __import__('importnb').Notebook(): 
        import readme
```

#### or explicity 


```python
    from importnb import Notebook
    with Notebook(): 
        import readme
```


```python
    foo = 42
    import readme
    assert readme.foo is 42
    assert readme.__file__.endswith('.ipynb')
```

### Modules may be reloaded 

The context manager is required to `reload` a module.


```python
    from importlib import reload
    with Notebook():
        reload(readme)
```

### Partial loading

The [`importnb.loader.Notebook`](src/notebooks/loader.ipynb#Partial-Loader) will __import__ a notebook even if there is an exception by supplying the `exceptions` option.  The __exception__ is found on `module._exception`.


```python
    with Notebook(exceptions=BaseException):
        try: from . import readme
        except: import readme
```

### Lazy imports

The `lazy` option will delay the evaluation of a module until one of its attributes are accessed the first time.


```python
    with Notebook(lazy=True):
        import readme
```

## Capture Outputs

`importnb` can capture the `stdout`, `stderr`, and `display` in the context manager.  The arguments are similar to `IPython.util.capture.capture_output`.


```python
    with Notebook(stdout=True, stderr=True, display=True) as output:
        import readme
```

### Docstring

The first markdown cell will become the module docstring.


```python
    if __name__ == '__main__':
        print(readme.__doc__.splitlines()[0])
```

    __importnb__ imports notebooks as modules & packages.


Meaning non-code blocks can be executeb by [doctest]().


```python
    if __name__ == '__main__':
        __import__('doctest').testmod(readme)
```

# Import notebooks from files

Notebook names may not be valid Python paths.  In this case, use `Notebook.from_filename`.

       Notebook.from_filename('readme.ipynb')
       
Import under the `__main__` context.
       
       Notebook.from_filename('readme.ipynb', main=True)

# Parameterize Notebooks

Literal ast statements are converted to notebooks parameters.

In `readme`, `foo` is a parameter because it may be evaluated with ast.literal_val


```python
    from importnb import Parameterize
    f = Parameterize().from_filename(readme.__file__)
    
```

The parameterized module is a callable that evaluates with different literal statements.


```python
    assert callable(f)
    f.__signature__
```




    <Signature (*, foo=42)>



    assert f().foo == 42
    assert f(foo='importnb').foo == 'importnb'

# Run Notebooks from the command line

Run any notebook from the command line with importnb.  Any parameterized expressions are available as parameters on the command line.

    !ipython -m importnb -- readme.ipynb --foo "I'm the new foo"
    !python -m importnb readme.ipynb --foo "No I am!"
    
After installing the IPython Extension any notebook may be run as any a command line script

    !ipython -m readme -- --foo "look at me"


## Integrations


### IPython

#### [IPython Extension](src/notebooks/loader.ipynb#IPython-Extensions)

Avoid the use of the context manager using loading importnb as IPython extension.

    %load_ext importnb
    
`%unload_ext importnb` will unload the extension.

#### Default Extension

`importnb` may allow notebooks to import by default with 

    importnb-install
    
This extension will install a script into the default IPython profile startup that is called each time an IPython session is created.  

Uninstall the extension with `importnb-install`.

##### Run a notebook as a module

When the default extension is loaded any notebook can be run from the command line. After the `importnb` extension is created notebooks can be execute from the command line.

    ipython -m readme
    
In the command line context, `__file__ == sys.arv[0] and __name__ == '__main__'` .
    
> See the [deploy step in the travis build](https://github.com/deathbeds/importnb/blob/docs/.travis.yml#L19).

### py.test

`importnb` installs a pytest plugin when it is setup.  Any notebook obeying the py.test discovery conventions can be used in to pytest.  _This is great because notebooks are generally your first test._

    !ipython -m pytest -- src 
    
Will find all the test notebooks and configurations as pytest would any Python file.

### Setup

To package notebooks add `recursive-include package_name *.ipynb`

## Developer

* [Source Notebooks](src/notebooks/)
* [Transpiled Python Source](src/importnb/)
* [Tests](src/importnb/tests)

### Format and test the Source Code


```python
    if __name__ == '__main__':
        from subprocess import call
        from importnb.capture import capture_output
        with capture_output() as out:  __import__('pytest').main("src".split())
        print('plugins'+out.stdout.split('plugins', 1)[-1])
            
        if 'kernel' in __import__('sys').argv[0]:
            """Formatting"""
            from pathlib import Path
            from importnb.utils.export import export
            root = 'src/importnb/notebooks/'
            for path in Path(root).rglob("""*.ipynb"""):                
                if 'checkpoint' not in str(path):
                    export(path, Path('src/importnb') / path.with_suffix('.py').relative_to(root))
            call("jupyter nbconvert --to markdown --NbConvertApp.output_files_dir=docs/{notebook_name}_files readme.ipynb".split())
        else:
            print(foo)
```

    plugins: cov-2.5.1, benchmark-3.1.1, hypothesis-3.56.5, importnb-0.3.0
    collecting ... collected 25 items
    
    src/importnb/tests/test_importnb.ipynb::test_single_file_with_context PASSED [  4%]
    src/importnb/tests/test_importnb.ipynb::test_from_filename PASSED      [  8%]
    src/importnb/tests/test_importnb.ipynb::test_from_execute PASSED       [ 12%]
    src/importnb/tests/test_importnb.ipynb::test_with_doctest PASSED       [ 16%]
    src/importnb/tests/test_importnb.ipynb::test_from_filename_main PASSED [ 20%]
    src/importnb/tests/test_importnb.ipynb::test_parameterize PASSED       [ 24%]
    src/importnb/tests/test_importnb.ipynb::test_commandline PASSED        [ 28%]
    src/importnb/tests/test_importnb.ipynb::test_python_file PASSED        [ 32%]
    src/importnb/tests/test_importnb.ipynb::test_single_file_with_capture PASSED [ 36%]
    src/importnb/tests/test_importnb.ipynb::test_capturer PASSED           [ 40%]
    src/importnb/tests/test_importnb.ipynb::test_single_file_with_lazy PASSED [ 44%]
    src/importnb/tests/test_importnb.ipynb::test_single_file_without_context XPASS [ 48%]
    src/importnb/tests/test_importnb.ipynb::test_single_file_relative 42
    xfail [ 52%]
    src/importnb/tests/test_importnb.ipynb::test_single_with_extension PASSED [ 56%]
    src/importnb/tests/test_importnb.ipynb::test_package PASSED            [ 60%]
    src/importnb/tests/test_importnb.ipynb::test_package_failure xfail     [ 64%]
    src/importnb/tests/test_importnb.ipynb::test_package_failure_partial PASSED [ 68%]
    src/importnb/tests/test_importnb.ipynb::test_tmp_dir PASSED            [ 72%]
    src/importnb/tests/test_unittests.ipynb::TestExtension::test_failure xfail [ 76%]
    src/importnb/tests/test_unittests.ipynb::TestExtension::test_import PASSED [ 80%]
    src/importnb/tests/test_unittests.ipynb::TestContext::test_import PASSED [ 84%]
    src/importnb/tests/test_unittests.ipynb::TestContext::test_reload_with_context PASSED [ 88%]
    src/importnb/tests/test_unittests.ipynb::TestPartial::test_exception PASSED [ 92%]
    src/importnb/tests/test_unittests.ipynb::TestPartial::test_traceback PASSED [ 96%]
    src/importnb/tests/test_unittests.ipynb::TestRemote::test_imports SKIPPED [100%]
    
    ---------- coverage: platform darwin, python 3.6.3-final-0 -----------
    Name                                                      Stmts   Miss  Cover
    -----------------------------------------------------------------------------
    src/importnb/Untitled.py                                      3      3     0%
    src/importnb/__init__.py                                     11     11     0%
    src/importnb/__main__.py                                      3      3     0%
    src/importnb/_version.py                                      1      1     0%
    src/importnb/capture.py                                      59     59     0%
    src/importnb/execute.py                                      92     49    47%
    src/importnb/loader.py                                      153     88    42%
    src/importnb/notebooks/__init__.py                            0      0   100%
    src/importnb/notebooks/utils/__init__.py                      0      0   100%
    src/importnb/parameterize.py                                100     63    37%
    src/importnb/path_hooks.py                                   84     34    60%
    src/importnb/test.py                                         57     57     0%
    src/importnb/usage/__init__.py                                0      0   100%
    src/importnb/usage/a_project_with_notebooks/__init__.py       2      2     0%
    src/importnb/usage/a_project_with_notebooks/foobaz.py         5      5     0%
    src/importnb/utils/__init__.py                                0      0   100%
    src/importnb/utils/export.py                                 33     33     0%
    src/importnb/utils/ipython.py                                41     41     0%
    src/importnb/utils/nbdoctest.py                              36     36     0%
    src/importnb/utils/pytest_plugin.py                          21     12    43%
    src/importnb/utils/setup.py                                  52     52     0%
    -----------------------------------------------------------------------------
    TOTAL                                                       753    549    27%
    
    
    ========= 20 passed, 1 skipped, 3 xfailed, 1 xpassed in 3.93 seconds =========
    



```python
    if __name__ == '__main__':
        try:
            from IPython.display import display, Image
            from IPython import get_ipython
            with capture_output(): 
                get_ipython().system("cd docs && pyreverse importnb -opng -pimportnb")
            display(Image(url='docs/classes_importnb.png', ))
        except: ...
```


<img src="docs/classes_importnb.png"/>

