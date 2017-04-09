#!/bin/bash

cd /opt/ctf/pokemon/rw

if [[ "i386" == "x86_64" ]] || [[ "x86_64" == "x86_64" ]] ; then
  ../ro/pokemon 2>/dev/null
else
  qemu-x86_64 ../ro/pokemon 2>/dev/null
fi