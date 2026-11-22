#!/bin/bash
# Run this once from the Homepage directory to download all external images locally.
# After running, commit images/banner/ and images/people/ to git.

set -e
cd "$(dirname "$0")"

mkdir -p images/banner images/people

echo "Downloading banner images..."

curl -# -o images/banner/Mathematikon.jpg \
  "https://drupal.mathinf-old.uni-heidelberg.de/sites/default/files/2021-08/Mathematikon.jpg"

curl -# -o images/banner/Rundgang1_0.jpg \
  "https://drupal.mathinf-old.uni-heidelberg.de/sites/default/files/2021-08/Rundgang1_0.jpg"

curl -# -o images/banner/MegaMenuStudies_0.jpg \
  "https://drupal.mathinf-old.uni-heidelberg.de/sites/default/files/2021-08/MegaMenuStudies_0.jpg"

curl -# -o images/banner/MegaMenuFaculty_0.jpg \
  "https://drupal.mathinf-old.uni-heidelberg.de/sites/default/files/2021-08/MegaMenuFaculty_0.jpg"

curl -# -o images/banner/mathematikon_abend.jpeg \
  "https://backend.math.uni-heidelberg.de/sites/default/files/2023-03/40a23815-85a1-4f66-bedf-ff1945c4c4d1_rw_1920.jpeg"

curl -# -o images/banner/mathematikon_skulptur.jpeg \
  "https://backend.math.uni-heidelberg.de/sites/default/files/2023-03/dc1e0054-cf9c-454c-a055-b163f220c9c5_rw_1920.jpeg"

curl -# -o images/banner/mathematikon_innenhof.jpeg \
  "https://backend.math.uni-heidelberg.de/sites/default/files/2023-03/mathematikon_innenhof.jpeg"

# Campus panorama (Neuenheimer Feld aerial view, CC BY-SA 4.0, Rolf Kickuth via Wikimedia Commons)
curl -# -o images/banner/campus_neuenheimer_feld.jpg \
  "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/HeidelbergUniCampusNeuenheimerFeld2020-07-22-13-08-03.jpg/1280px-HeidelbergUniCampusNeuenheimerFeld2020-07-22-13-08-03.jpg"

echo "Downloading person photos..."

curl -# -o images/people/Anna_Marciniak_Czochra.png \
  "https://backend.math.uni-heidelberg.de/sites/default/files/styles/img_16_9_aspect_0375/public/2023-04/Anna_Marciniak_Czochra.PNG?h=ede675b1&itok=_0mBT_qg"

curl -# -o images/people/Jan_Fuhrmann.jpg \
  "https://backend.math.uni-heidelberg.de/sites/default/files/styles/img_16_9_aspect_0375/public/2024-11/Jan_Fuhrmann.jpg?h=ae285db8&itok=48wW7rHB"

curl -# -o images/people/Tim_Laux_wide_0.jpg \
  "https://backend.math.uni-heidelberg.de/sites/default/files/styles/img_16_9_aspect_0375/public/2025-09/Tim_Laux_wide_0.jpg?h=a0ac5f3f&itok=3cQzkW3u"

echo ""
echo "Done. Files:"
ls -lh images/banner/ images/people/
