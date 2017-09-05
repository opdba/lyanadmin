#!/usr/bin/env python
# -*- coding:utf-8 -*-
import platform
import sys

from plugin import plugin_api


class Collect_Info(object):

    def get_platform(self):
        action_platform = platform.system()
        return action_platform

    def collect(self):
        action_platform = self.get_platform()
        try:
            func = getattr(self,action_platform)
            data = func()  #最终返回大字典

            return data

        except AttributeError as e:
            sys.exit("Error:",e)


    def Linux(self):
        sys_info = plugin_api.LinuxInfo()
        return sys_info


    def Windows(self):
        sys_info = plugin_api.Windows_Info()
        return sys_info



