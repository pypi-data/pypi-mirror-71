#!/bin/sh
#
# This file is part of REANA.
# Copyright (C) 2018 CERN.
#
# REANA is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

pydocstyle reana_db && \
black --check . && \
check-manifest --ignore ".travis-*" && \
sphinx-build -qnNW docs docs/_build/html && \
REANA_SQLALCHEMY_DATABASE_URI=sqlite:// python setup.py test && \
sphinx-build -qnNW -b doctest docs docs/_build/doctest
