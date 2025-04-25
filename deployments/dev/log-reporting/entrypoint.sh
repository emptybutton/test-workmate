#!/bin/bash

uv sync --extra dev
source ${UV_PROJECT_ENVIRONMENT}/bin/activate
$@
