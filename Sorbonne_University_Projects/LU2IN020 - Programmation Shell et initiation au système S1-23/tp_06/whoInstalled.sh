#!/bin/bash

grep '^[^:]*:[^:]*:1000:' /etc/passwd | cut -d ':' -f1
