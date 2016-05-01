# backend.py - compile LaTeX file to PDF, optionally open in viewer

import os
import platform
import subprocess

from .._compat import apply, range

from . import tools

__all__ = ['compile']

PLATFORM = platform.system().lower()


def no_compile(filename, view=False):
    raise NotImplementedError('platform not supported')


def pdflatex_compile(filename, view=False):
    """Compile LaTeX file by running pdflatex three times."""
    pdflatex = ['pdflatex', '-output-format=pdf', '-interaction=batchmode', '-halt-on-error']
    compile_dir = os.path.dirname(filename)
    if compile_dir:
        pdflatex.append('-output-directory=%s' % compile_dir)
    pdflatex.append(filename)

    for i in range(3):
        subprocess.call(pdflatex)
    if view:
        open_viewer(tools.swapext(filename, 'pdf'))


def latexmk_compile(filename, view=False):
    """Compile LaTeX file with the latexmk perl script."""
    compile_dir, filename = os.path.split(filename)

    latexmk = ['latexmk', '-pdf', '-silent']
    if view:
        latexmk.append('-pv')
    latexmk.append(filename)

    with tools.chdir(compile_dir):
        subprocess.call(latexmk)


def texify_compile(filename, view=False):
    """Compile LaTeX file using MikTeX's texify utility."""
    compile_dir, filename = os.path.split(filename)  # texify has issues with remote directory

    texify = ['texify', '--pdf', '--batch', '--verbose', '--quiet']
    if view:
        texify.append('--run-viewer')
    texify.append(filename)

    with tools.chdir(compile_dir):
        subprocess.call(texify)


@apply
def compile(platform=PLATFORM):
    compile_funcs = {
        'darwin': pdflatex_compile,
        'linux': pdflatex_compile,
        'windows': texify_compile,
    }
    return compile_funcs.get(platform, no_compile)


def no_view(filepath):
    raise NotImplementedError('platform not supported')


def view_darwin(filepath):
    """Open filepath with its default application (mac)."""
    subprocess.Popen(['open', filepath])


def view_linux(filepath):
    """Open filepath in the user's preferred application (linux)."""
    subprocess.Popen(['xdg-open', filepath])


def view_windows(filepath):
    """Start filepath with its associated application (windows)."""
    os.startfile(os.path.normpath(filepath))


@apply
def open_viewer(platform=PLATFORM):
    view_funcs = {
        'darwin': view_darwin,
        'linux': view_linux,
        'windows': view_windows,
    }
    return view_funcs.get(platform, no_view)
