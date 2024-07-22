#!/usr/bin/env bash
# exit on error
set -o errexit

STORAGE_DIR=$HOME/project/src
CHROME_DIR=$STORAGE_DIR/chrome
CHROMEDRIVER_DIR=$STORAGE_DIR/chromedriver
echo "Running Script.sh .."

if [[ ! -d $CHROME_DIR || ! -d $CHROMEDRIVER_DIR ]]; then
  echo "...Downloading Chrome and ChromeDriver"
  
  # Create directories if they do not exist
  mkdir -p $CHROME_DIR
  mkdir -p $CHROMEDRIVER_DIR

  # Download and unzip Chrome
  wget -P $CHROME_DIR https://storage.googleapis.com/chrome-for-testing-public/126.0.6478.126/linux64/chrome-linux64.zip
  unzip $CHROME_DIR/chrome-linux64.zip -d $CHROME_DIR
  rm $CHROME_DIR/chrome-linux64.zip

  
  # Download and unzip ChromeDriver
  wget -P $CHROMEDRIVER_DIR https://storage.googleapis.com/chrome-for-testing-public/126.0.6478.126/linux64/chromedriver-linux64.zip
  unzip $CHROMEDRIVER_DIR/chromedriver-linux64.zip -d $CHROMEDRIVER_DIR
  rm $CHROMEDRIVER_DIR/chromedriver-linux64.zip


  # Change permissions to read and write for all users 
  chmod -R 777 $CHROME_DIR
  chmod -R 777 $CHROMEDRIVER_DIR

  echo "Atharva Chrome and ChromeDriver downloaded"
  echo " atharva home "+ $HOME 
  pwd $CHROME_DIR
  pwd $CHROMEDRIVER_DIR
  ls -l $CHROME_DIR
  ls -l $CHROMEDRIVER_DIR

  echo "Atharva Done printing directories"
  $CHROME_DIR/chrome-linux64/chrome --version
else
  echo "...Using Chrome and ChromeDriver from cache"
  ls -l $CHROME_DIR
  ls -l $CHROMEDRIVER_DIR
fi

echo "Ended Script.sh .."
