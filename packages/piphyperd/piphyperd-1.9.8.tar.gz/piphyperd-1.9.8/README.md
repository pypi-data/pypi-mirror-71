# piphyperd

[![pipeline status](https://gitlab.com/hyperd/piphyperd/badges/master/pipeline.svg)](https://gitlab.com/hyperd/piphyperd/commits/master)

[![pylint](https://gitlab.com/hyperd/piphyperd/-/jobs/artifacts/master/raw/pylint/pylint.svg?job=pylint)](https://gitlab.com/hyperd/piphyperd/commits/master)

![Python package](https://github.com/hyp3rd/piphyperd/workflows/Python%20package/badge.svg)

A simple python package to leverage pip programmatically, and via CLI.
**piphyperd** is a wrapper around **pip**; it can provide features like automation or dependencies control within your workflows.

## About this package

The reasons behind this package, in alternative to the standard `pip` (`import pip`) module, are in the attempt to expose a more stable interface, when programmatically installing or managing python packages, within pipelines or automation workflows.

Although it is a **Python** module, and it is available via `import pip`, by design, **pip** is not supposed to be a library; every detail is subject to changes for any reason, from the import name itself to its API. It might be better to call the pip's internal APIs differently.

### Pitfalls

When leveraging `pip` programmatically, there are also other topics worth considering:

1. The pip code assumes that it is in sole control of the global state of the program;
2. pip's code is not thread-safe. If you were to run pip in a thread;
3. pip assumes that once it has finished its work, the process terminates.

Furthermore, installing packages under the `sys.path` from a running Python process might result in unexpected or undesired behaviors.

Taking everything into account, still might be necessary, or usefull, handling pip packages within code and automations, as much as possible in controlled manner. The most reliable way to do so, is leveraging pip in a `subprocess`:

```python
# leverage subprocess.Popen to execute pip commands
pip_full_cmd: Union[Any] = sorted(
    self.pip_options + self.packages + self.command_args)

process = subprocess.Popen(
    [sys.executable if self.python_path is None
        else self.python_path,
        "-m", "pip", command] + pip_full_cmd,
    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
```

For further information, continue reading from the source of this topic at the [the official pypa](https://pip.pypa.io/en/latest/user_guide/#using-pip-from-your-program) user guide.

## Install the package

Refer to the official [project page](https://pypi.org/project/piphyperd/) for further information about the package status and releases.

To install the latest version, run the following command in your terminal:

```bash
pip install --user piphyperd
```

## API overview

Once installed, you can import the package as follows `from piphyperd import PipHyperd`.
The module is wrapping pip commands in methods, exposed through the object `PipHyperd`. You can initialize it by optionally passing pip commands extra options:

```python
def __init__(self, *pip_options: Any, python_path: Optional[Path] = None):
    """Init method."""
    # Path to the python binary to use
    self.python_path: Optional[Path] = python_path
    # A list of pip packages to install || show || download || uninstall
    self.packages: List[str] = list()
    # pip command args, e.g.: pip download testpypi {command_args}
    self.command_args: List[str] = list()
    # pip options, e.g.: pip {pip_options} uninstall testpypi
    self.pip_options: List[str] = list(pip_options)
# ...
```

The API exposed conveniently wraps a set of pip commands that can help generating virtual environments, reports of the installed packages, outdated libraries. The `stdout` and `stderr` are returned by each method, allowing to store the output or to read it in a second instance.

### Object description

To follow, a brief walkthrough through the methods exposed by the `PipHyperd` object, **programmatically** and via the **CLI**

#### pip freeze

Output installed pip packages in requirements format:

```python
# python
piphyperd.PipHyperd().freeze()
```

```bash
# cli
piphyperd freeze
```

#### pip list

List installed pip packages.

list_outdated -- True || False to list or not the outdated packages

```python
# python
piphyperd.PipHyperd("--verbose").list_packages() # the argument "--verbose" is of course optional

# List outdated packages
piphyperd.PipHyperd().list(True)
```

```bash
# cli
piphyperd list
```

#### pip show {{ package }}

Show information about installed packages.

```python
# python
piphyperd.PipHyperd("--verbose").show("ansible")
```

```bash
# cli
piphyperd show --package <package_name>
```

#### pip check

Verify installed packages have compatible dependencies.

```python
# python
piphyperd.PipHyperd().check()
```

```bash
# cli
piphyperd check
```

#### pipdeptree

Render installed packages with dependencies tree.

```python
# python
piphyperd.PipHyperd().dependencies_tree()
```

```bash
# cli
piphyperd dependencies-tree
```

#### pip install {{ packages }}

Install pip packages.

```python
# python
piphyperd.PipHyperd("-U").install("ansible", "cryptography") # -U is of course optional, set here as example
```

```bash
# cli
piphyperd install --packages <package_name_1> <package_name_2> <package_name_n>
piphyperd install --package <package_name>
```

#### pip download {{ package }}

Download pip packages.

```python
# python
piphyperd.PipHyperd("-U").download("ansible", "pip", "cryptography", destination="/your/path/here") # the destination argument is optional
```

```bash
# cli
piphyperd download --package twine==3.1.1
```

#### pip uninstall {{ packages }}

Uninstall pip packages.

```python
piphyperd.PipHyperd().uninstall("ansible", "pip", "cryptography") # the destination argument is optional
```

```bash
# cli
piphyperd uninstall --packages <package_name_1> <package_name_2> <package_name_n>
piphyperd uninstall --package <package_name>
```

## License

[GNU General Public License v3 (GPLv3)](https://gitlab.com/hyperd/piphyperd/blob/master/LICENSE)

## Report a Vulnerability

If you believe you have found a security vulnerability in **venvctl**, refer to the [Tidelift security policy](https://tidelift.com/docs/security).

The **Tidelift** team will coordinate the vunerability response and disclosure.

## Author Information

[Francesco Cosentino](https://www.linkedin.com/in/francesco-cosentino/)

I'm a surfer, a crypto trader, and a DevSecOps Engineer with 15 years of experience designing highly-available distributed production environments and developing cloud-native apps in public and private clouds.
