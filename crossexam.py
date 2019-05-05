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

if shutil.which('meson'):
    meson_bin = 'meson'
elif 'MESON_EXE' in os.environ:
    meson_bin = os.environ['MESON_EXE']
else:
    meson_bin = '/home/jpakkane/workspace/meson/meson.py'

def write_chains(ninjafile):
    ninjafile.write('''build first_build: run_command
 command = %s ../cc first_build
 
build first: run_command | first_build
 command = ninja -C first_build

build clean_first: run_command | first_build
 command = ninja -C first_build clean

'''  % meson_bin)

    ninjafile.write('''build second_build: run_command | first_build
 command = CC=%s/first_build/newcc %s ../cc second_build
 
build second: run_command | second_build
 command = ninja -C second_build

build clean_second: run_command | second_build
 command = ninja -C second_build clean
''' % (os.getcwd()+ '/chainbuild', meson_bin))

def write_helpers(ninjafile):
    ninjafile.write('build all: phony first second \n')
    ninjafile.write('build clean: phony clean_first clean_second\n')
    ninjafile.write('default all\n')

def setup_compiler_chain():
    chaindir = pathlib.Path('chainbuild')
    if chaindir.is_dir():
        shutil.rmtree(chaindir)
    os.mkdir(chaindir)
    with (chaindir / 'build.ninja').open('w') as ninjafile:
        ninjafile.write('''ninja_required_version = 1.8.2
rule run_command
 command = $command
 description = $desc
 restat = 1
''')
        write_chains(ninjafile)
        write_helpers(ninjafile)

if __name__ == '__main__':
    assert(os.path.isdir('cc'))
    setup_compiler_chain()
