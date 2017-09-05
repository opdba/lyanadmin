#!/usr/bin/env python
# -*- coding:utf-8 -*-

def LinuxInfo():
    from linux import sysinfo
    return sysinfo.collect()


def Windows_Info():
    from windows import sysinfo
    return sysinfo.collect()

