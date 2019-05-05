#!/usr/bin/env python3

# Copyright 2019 Jussi Pakkanen

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os, sys, subprocess, shutil, pathlib

ninja_header = '''ninja_required_version = 1.8.2
rule run_command
 command = $command
 description = $desc
 restat = 1
'''

if shutil.which('meson'):
    meson_bin = 'meson'
elif 'MESON_EXE' in os.environ:
    meson_bin = os.environ['MESON_EXE']
else:
    meson_bin = '/home/jpakkane/workspace/meson/meson.py'

def write_chains(ninjafile, elements):
    for i, elem in enumerate(elements):
        if i == 0:
            ninjafile.write('''build %s_build: run_command
 command = %s ../cc %s_build
 pool = console
''' % (elem, meson_bin, elem))

            ninjafile.write('''build %s: run_command | %s_build
 command = ninja -C %s_build
 pool = console
''' % (elem, elem, elem))
            
            ninjafile.write('''build clean_%s: run_command | %s_build
 command = ninja -C %s_build clean
 pool = console

'''  % (elem, elem, elem))

        else:
            prev_cc = os.getcwd() + '/chainbuild/%s_build/newcc' % elements[i-1]
            ninjafile.write('''build %s_build: run_command | %s_build
 command = CC=%s %s ../cc %s_build -Dactual=%s
 pool = console
''' % (elem, elements[i-1], prev_cc, meson_bin, elem, prev_cc))

            ninjafile.write('''build %s: run_command | %s_build
 command = ninja -C %s_build
 pool = console
''' % (elem, elem, elem))

            ninjafile.write('''build clean_%s: run_command | %s_build
 command = ninja -C %s_build clean
 pool = console

''' % (elem, elem, elem))

def write_helpers(ninjafile, elements):
    ninjafile.write('build all: phony {}\n'.format(' '.join(elements)))
    ninjafile.write('build clean: phony {}\n'.format(' '.join(['clean_' + x for x in elements])))
    ninjafile.write('build install: phony {}\n'.format(' '.join(['install_' + x for x in elements])))
    ninjafile.write('default all\n')

def setup_compiler_chain():
    chaindir = pathlib.Path('chainbuild')
    if chaindir.is_dir():
        shutil.rmtree(chaindir)
    os.mkdir(chaindir)
    with (chaindir / 'build.ninja').open('w') as ninjafile:
        ninjafile.write(ninja_header)
        elements = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth']
        write_chains(ninjafile, elements)
        write_helpers(ninjafile, elements)

def setup_multilib():
    # Emulates an Android compile with one jar + multiple shared libs.
    fauxdir = pathlib.Path('fauxbuild')
    if fauxdir.is_dir():
        shutil.rmtree(fauxdir)
    os.mkdir(fauxdir)
    with (fauxdir / 'build.ninja').open('w') as ninjafile:
        native = 'x86_64'
        ninjafile.write(ninja_header)
        ninjafile.write('''build %s_build: run_command
 command = %s ../fauxdroid %s_build -Dbuild_java=true --prefix=/usr --libdir=lib/x86_64
 pool = console
''' % (native, meson_bin, native))

        ninjafile.write('''build %s: run_command | %s_build
 command = ninja -C %s_build
 pool = console
''' % (native, native, native))

        ninjafile.write('''build clean_%s: run_command
 command = ninja -C %s_build clean
 pool = console
''' % (native, native))

        ninjafile.write('''build install_%s: run_command | %s_build
 command = ninja -C %s_build install
 pool = console

'''  % (native, native, native))

        cross = 'arm'
        ninjafile.write('''build %s_build: run_command
 command = %s --cross-file %s/ubuntu-armhf.txt --prefix=/usr --libdir=lib/arm ../fauxdroid %s_build
 pool = console
''' % (cross, meson_bin, os.getcwd(), cross))

        ninjafile.write('''build %s: run_command | %s_build
 command = ninja -C %s_build
 pool = console
''' % (cross, cross, cross))

        ninjafile.write('''build clean_%s: run_command
 command = ninja -C %s_build clean
 pool = console
''' % (cross, cross))

        ninjafile.write('''build install_%s: run_command | %s_build
 command = ninja -C %s_build install
 pool = console

'''  % (cross, cross, cross))
        write_helpers(ninjafile, ['x86_64', 'arm'])

if __name__ == '__main__':
    assert(os.path.isdir('cc'))
    setup_compiler_chain()
    setup_multilib()

