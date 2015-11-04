# pdflatex.py - render LaTeX file to PDF and optionally open in viewer

import sys
import os
import subprocess

from . import tools

__all__ = ['render', 'viewer']

VIEW = False


def no_compile(filename, view=VIEW):
    raise NotImplementedError('unsupported platform')


def texlive_compile(filename, view=VIEW):
    pdflatex = ['pdflatex', '-pdf', '-interaction=batchmode', '-halt-on-error']
    compile_dir = os.path.dirname(filename)
    if compile_dir:
        pdflatex.append('-output-directory=%s' % compile_dir)
    pdflatex.append(filename)
    for i in range(3):
        subprocess.Popen(pdflatex).wait()
    if view:
        viewer(tools.swapext(filename, 'pdf'))


def miktex_compile(filename, view=VIEW):
    compile_dir, filename = os.path.split(filename)  # texify has issues with remote directory
    texify = ['texify', '--pdf', '--batch', '--verbose', '--quiet']
    if view:
        texify.append('--run-viewer')
    texify.append(filename)
    with tools.chdir(compile_dir):
        subprocess.Popen(texify).wait()


@apply
def render(platform=sys.platform):
    compile_funcs = {
        'darwin': texlive_compile,
        'linux2': texlive_compile,
        'win32': miktex_compile,
    }
    return compile_funcs.get(platform, no_compile)


def no_view(filepath):
    raise NotImplementedError('unsupported platform')


def darwin_view(filepath):
    subprocess.Popen(['open', filepath])


def linux2_view(filepath):
    subprocess.Popen(['xdg-open', filepath])


def win32_view(filepath):
    os.startfile(os.path.normpath(filepath))


@apply
def viewer(platform=sys.platform):
    view_funcs = {
        'darwin': darwin_view,
        'linux2': linux2_view,
        'win32': win32_view,
    }
    return view_funcs.get(platform, no_view)
