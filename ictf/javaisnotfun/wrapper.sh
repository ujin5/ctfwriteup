#!/bin/bash

cd /opt/ctf/javaisnotfun/rw

if [[ "i386" == "x86_64" ]] || [[ "x86_64" == "x86_64" ]] ; then
  ../ro/javaisnotfun 2>/dev/null
else
  qemu-x86_64 ../ro/javaisnotfun 2>/dev/null
fi