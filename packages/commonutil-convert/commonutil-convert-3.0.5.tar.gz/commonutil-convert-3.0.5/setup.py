#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup  # pylint: disable=import-error

setup(
		name="commonutil-convert",
		version="3.0.5",  # REV-CONSTANT:rev 5d022db7d38f580a850cd995e26a6c2f
		description="Data instance convert routines",
		packages=[
				"commonutil_convert",
		],
		classifiers=[
				"Development Status :: 5 - Production/Stable",
				"Intended Audience :: Developers",
				"License :: OSI Approved :: MIT License",
				"Operating System :: POSIX",
				"Programming Language :: Python :: 3.6",
				"Programming Language :: Python :: 3.7",
		],
		license="MIT License",
)
