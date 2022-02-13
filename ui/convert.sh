#!/bin/bash

path="${0%/*}"
raw="${path}/raw"
converted="${path}/converted"

if ! command -v pyuic5 &>/dev/null; then
  echo "\"pyuic5\" is not found!"
  echo "PyQT dev tools are not installed!"
  exit 1
fi

if [ ! -d "${raw}" ]; then
  echo "directory \"raw\" doesn't exist!"
  exit 2
fi

if [ ! -d "${converted}" ]; then
  echo "directory \"converted\" doesn't exist!"
  exit 3
fi

ui_files="${path}/raw/*.ui"
for ui_file in $ui_files; do
  file=$(basename "${ui_file}" .ui)
  py_file="${converted}/${file}.py"

  if pyuic5 "$ui_file" -o "$py_file"; then
    echo "\"${ui_file}\" converted into \"${py_file}\""
  else
    echo "failed to convert \"${ui_file}\" into \"${py_file}\"!"
    exit 4
  fi
done
