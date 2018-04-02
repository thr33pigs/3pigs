#!/usr/bin/env python
# encoding: utf-8

import re
import hashlib
from time import sleep

def alert(error):
    return "<script>alert('%s');location.href='/index.php'</script>"%(error)

def MD5(s):
    return hashlib.md5(s).hexdigest()


def checklogin(post,vcode):
    if post['username'] and post['vcode']:
        u = post['username']
        v = post['vcode']
        return MD5(v)[:4] == vcode
