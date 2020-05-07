#!/bin/bash

DIR="$( cd "$( dirname "$0" )" && pwd )"

pushd $DIR
pip3 install .

application_filename=braphy.desktop
application_directory=~/.local/share/applications
application_file=$application_directory/$application_filename

cat > $application_file << EOL
#!/usr/bin/env xdg-open

[Desktop Entry]
Type=Application
Terminal=false
Exec=$(pwd)/bin/braphy.sh
Name=braphy
EOL

chmod +x $application_file

popd
