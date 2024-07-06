#!/usr/bin/env bash
# exit on error
set -o errexit

STORAGE_DIR=/opt/render/project/.render
echo "Running Script.sh .."

if [[ ! -d $STORAGE_DIR/chrome ]]; then
  echo "...Downloading Chrome"
  mkdir -p $STORAGE_DIR/chrome
  cd $STORAGE_DIR/chrome
  wget -P ./ https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  dpkg -x ./google-chrome-stable_current_amd64.deb $STORAGE_DIR/chrome
  rm ./google-chrome-stable_current_amd64.deb
  cd $HOME/project/src # Make sure we return to where we were

  
  echo "check Atharva"
  echo "$STORAGE_DIR/chrome/opt/google/chrome"  +" Atharva "
  ls -l $STORAGE_DIR/chrome/ +" Atharva "
  echo $PWD +" Atharva "

  # Output the path to Chromium
  echo "check"
  echo $PATH
  ls -l $STORAGE_DIR/chrome/opt/google/chrome  +" Atharva "


else
  ls -l $STORAGE_DIR/chrome/opt/google/chrome
  ls -l $STORAGE_DIR/chrome/

  echo "...Using Chrome from cache"
fi

echo "Ended Script.sh .."