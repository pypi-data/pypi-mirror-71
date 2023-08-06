#!/usr/bin/python
#
# Print the compile-time software build version of the CMS manager.
#
from __future__ import print_function, absolute_import, unicode_literals
from dgpy.cms_client import CmsClient

print("CMS Build Version: ", CmsClient().build_version())
print("Python SDK Version:", CmsClient.version())
