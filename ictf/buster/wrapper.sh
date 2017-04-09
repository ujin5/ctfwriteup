#!/bin/bash

cd /opt/ctf/buster/rw

if [[ "i386" == "x86_64" ]] || [[ "x86_64" == "x86_64" ]] ; then
  ../ro/buster 2>/dev/null
else
  qemu-x86_64 ../ro/buster 2>/dev/null
fi