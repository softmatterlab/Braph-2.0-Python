#!/bin/bash

DIR="$( cd "$( dirname "$0" )" && pwd )"

pushd $DIR
pip3 install .

popd