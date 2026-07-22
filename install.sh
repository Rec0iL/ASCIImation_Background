#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="$HOME/.local/share/plasma/wallpapers/org.kde.plasma.starwars"

echo "=== Installing ASCIImation KDE Plasma Wallpaper & Lock Screen Plugin ==="

cd "$SCRIPT_DIR"

if [ ! -f "starwars.txt" ]; then
    echo "Fetching starwars.txt..."
    python3 -c "
import urllib.request
url = 'https://raw.githubusercontent.com/mgracanin/ASCIIStarWars/master/starwars.txt'
print('Downloading asciimation dataset from', url)
data = urllib.request.urlopen(url).read()
with open('starwars.txt', 'wb') as f:
    f.write(data)
"
fi

echo "Building QML animations library (Star Wars, Nyan Cat, Party Parrot, 3D Wireframe Cube)..."
python3 convert_all_animations.py

echo "Installing package to $TARGET_DIR..."
mkdir -p "$HOME/.local/share/plasma/wallpapers"

if command -v kpackagetool6 &>/dev/null; then
    echo "Registering plugin using kpackagetool6..."
    kpackagetool6 --type Plasma/Wallpaper --upgrade "$SCRIPT_DIR/org.kde.plasma.starwars" || \
    kpackagetool6 --type Plasma/Wallpaper --install "$SCRIPT_DIR/org.kde.plasma.starwars" || true
fi

echo "Copying plugin files..."
rm -rf "$TARGET_DIR"
cp -r "$SCRIPT_DIR/org.kde.plasma.starwars" "$TARGET_DIR"

echo "Clearing KDE QML cache..."
rm -rf ~/.cache/plasmashell/qmlcache ~/.cache/systemsettings/qmlcache ~/.cache/kcmshell6/qmlcache 2>/dev/null || true

echo ""
echo "=========================================================================="
echo " SUCCESS! ASCIImation Wallpaper & Lock Screen plugin is installed!"
echo "=========================================================================="
echo ""
echo "To set it as your Lock Screen Background in KDE Plasma 6:"
echo " 1. Open System Settings -> Screen Locking"
echo " 2. Click on 'Appearance' (Configure Lock Screen Appearance)"
echo " 3. Change 'Wallpaper Type' to 'ASCIImation'"
echo " 4. Choose your scene: Star Wars Episode IV, Nyan Cat, Party Parrot, 3D Cube"
echo " 5. Adjust phosphor colors, CRT scanlines, and speed, then click 'Apply'!"
echo "=========================================================================="
