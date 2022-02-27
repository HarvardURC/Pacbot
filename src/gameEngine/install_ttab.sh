#!/bin/bash

curl -LO https://raw.githubusercontent.com/mklement0/ttab/master/ttab.rb && 
HOMEBREW_NO_AUTO_UPDATE=1 brew install --formula ttab.rb && 
rm ttab.rb