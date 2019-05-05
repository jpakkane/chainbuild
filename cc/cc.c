/*
 Copyright 2019 Jussi Pakkanen

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
*/

#include<unistd.h>
#include<string.h>
#include<stdlib.h>
#include<stdio.h>

const char *actual_cc = ACTUAL_COMPILER;

int main(int argc, char **argv) {
    int i;
    char **actual_args = malloc(sizeof(char*)*10000);
    actual_args[0] = strdup(actual_cc);
    for(i=0; i<argc; i++) {
        actual_args[i] = strdup(argv[i]);
    }
    actual_args[i] = NULL;
    if(execv(actual_cc, actual_args) != 0) {
        perror(NULL);
    }
    return -1;
}
