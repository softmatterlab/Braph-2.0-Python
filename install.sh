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
Icon=$(pwd)/braphy/gui/icons/application_icon.png
Name=braphy
EOL

chmod +x $application_file

application_filename_kill=kill_braphy.desktop
application_kill=$application_directory/$application_filename_kill

cat > $application_kill << EOL
#!/usr/bin/env xdg-open

[Desktop Entry]
Type=Application
Terminal=false
Exec=$(pwd)/bin/kill_braphy.sh
Icon=$(pwd)/braphy/gui/icons/application_icon_kill.png
Name=kill braphy
EOL

chmod +x $application_kill

popd
