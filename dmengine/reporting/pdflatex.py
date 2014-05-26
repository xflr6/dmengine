# pdflatex.py - render LaTeX file to PDF

import sys
import os
import subprocess

from . import tools

__all__ = ['render', 'viewer']

VIEW = False


def texlive_compile(filename, view=VIEW):
    command = ['pdflatex', '-halt-on-error', '-interaction=batchmode']
    compile_dir = os.path.dirname(filename)
    if compile_dir:
        command.append('-output-directory=%s' % compile_dir)
    command.append(filename)
    for i in range(3):
        subprocess.Popen(command).wait()
    if view:
        viewer(tools.swapext(filename, 'pdf'))


def miktex_compile(filename, view=VIEW):
    command = ['texify', '--pdf', '--batch', '--verbose', '--quiet']
    if view:
        command.append('--run-viewer')
    if os.path.dirname(filename):  # texify has issues with remote directory
        compile_dir, filename = os.path.split(filename)
    else:
        compile_dir = None
    command.append(filename)
    with tools.chdir(compile_dir):
        return subprocess.Popen(command).wait()


def no_compile(filename, view=VIEW):
    raise NotImplementedError


@apply
def render(platform=sys.platform):
    compile_funcs = {
        'darwin': texlive_compile,
        'linux2': texlive_compile,
        'win32': miktex_compile,
    }
    return compile_funcs.get(platform, no_compile)


@apply
def viewer(platform=sys.platform):
    def darwin_view(filepath):
        subprocess.Popen(['open', filepath], shell=True)

    def linux2_view(filepath):
        subprocess.Popen(['xdg-open', filepath], shell=True)

    def win32_view(filepath):
        os.startfile(os.path.normpath(filepath))

    def no_view(filepath):
        raise NotImplementedError

    view_funcs = {
        'darwin': darwin_view,
        'linux2': linux2_view,
        'win32': win32_view,
    }
    return view_funcs.get(platform, no_view)
