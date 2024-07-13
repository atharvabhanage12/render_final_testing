#!/usr/bin/env bash
# exit on error
set -o errexit

STORAGE_DIR=/opt/render/project/.render
echo "Running Script.sh .."

if [[ ! -d $STORAGE_DIR/chrome ]]; then
  echo "...Downloading Chrome"
  mkdir -p $STORAGE_DIR/chrome
  cd $STORAGE_DIR/chrome


 # Download and unzip Chrome
  wget -P ./ https://storage.googleapis.com/chrome-for-testing-public/126.0.6478.126/linux64/chrome-linux64.zip
  unzip chrome-linux64.zip
  rm chrome-linux64.zip

  # Download and unzip ChromeDriver
  wget -P ./ https://storage.googleapis.com/chrome-for-testing-public/126.0.6478.126/linux64/chromedriver-linux64.zip
  unzip chromedriver-linux64.zip
  rm chromedriver-linux64.zip

  
  chmod -R 777 .
  chmod -R 777 $STORAGE_DIR/chrome
  ls
  ls -l $STORAGE_DIR/chrome/opt/google/chrome
  cd $HOME/project/src # Make sure we return to where we were

  # Change permissions to read and write for all users 
  ls -l . 
  chmod -R 777 $STORAGE_DIR/chrome
  echo "check Atharva"
  echo "$STORAGE_DIR/chrome/opt/google/chrome"  +" Atharva "
  $STORAGE_DIR/chrome/opt/google/chrome/google-chrome --version
  echo $PWD +" Atharva "
  ls -l $STORAGE_DIR/chrome/ 
  echo $PWD +" Atharva "

  # Output the path to Chromium
  echo "check" +" Atharva "
  echo $PATH +" Atharva "
  ls -l $STORAGE_DIR/chrome/opt/google/chrome 


else
  ls -l $STORAGE_DIR/chrome/opt/google/chrome
  ls -l $STORAGE_DIR/chrome/

  echo "...Using Chrome from cache"
fi

echo "Ended Script.sh .."

