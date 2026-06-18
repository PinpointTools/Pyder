#!/bin/bash

echo "This will install the compiled local 'guh' binary to '~/.local/bin' directory."
read -p "Do you want to continue? [y/n]: " choice

if [ "$choice" != "Y" ] && [ "$choice" != "y" ]; then
    echo "Installation cancelled."
    exit 0
fi

echo "Installing..."
echo

pyinstaller build.spec && echo "Successfully compiled 'pyder' binary." || echo "Failed to compile 'pyder' binary."
echo

cp dist/Pyder ~/.local/bin/pyder && echo "Successfully placed 'pyder' in '~/.local/bin' directory." || echo "Failed to place 'pyder' in '~/.local/bin' directory."
chmod +x ~/.local/bin/pyder && echo "Successfully made 'pyder' executable." || echo "Failed to make 'pyder' executable."

pyder version >> /dev/null && echo "Successfully installed 'pyder' binary." || echo "Failed to install 'pyder' binary."
echo "Installation complete."