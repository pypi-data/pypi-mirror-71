# coding=utf-8
import os
import re
import warnings

from BiliUtil.Util import Config

from BiliUtil.Space import User
from BiliUtil.Space import Channel

from BiliUtil.Video import Album
from BiliUtil.Video import Video

_aria2c_result = os.popen('aria2c -v').read()
_aria2c_result = re.match(r'(\S+)', _aria2c_result)
_ffmpeg_result = os.popen('ffmpeg -version').read()
_ffmpeg_result = re.match(r'(\S+)', _ffmpeg_result)
if _aria2c_result is not None and _aria2c_result.group(1) == 'aria2':
    if _ffmpeg_result is not None and _ffmpeg_result.group(1) == 'ffmpeg':
        from BiliUtil.Video import Task
        from BiliUtil.Video import Filter
        from BiliUtil.Video import Fetcher
    else:
        warnings.warn("QAQ~ 您未配置ffmpeg渲染环境，Task, Filter, Fetcher类不可用")
else:
    warnings.warn("QAQ~ 您未配置aria2c下载环境，Task, Filter, Fetcher类不可用")


