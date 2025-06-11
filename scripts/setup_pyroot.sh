#!/usr/bin/bash
# setup_pyroot.sh
#
# Script to set up environment for PyROOT (ROOT in Python 3).
#
# Run using either of the following commands:
#
# source setup_pyroot.sh 
#
# . setup_pyroot.sh
#
# Important: source or . are required to set environment variables in your terminal session!
#

# Alan Feltz installed a version of ROOT to use with PyROOT. 

# ROOT version for PyROOT installed on kucms:
#export ROOT_VER=root-6.30.04

# ROOT version for PyROOT installed on kucms-02:
export ROOT_VER=root-6.32.06

export ROOT_DIR=/usr/local/${ROOT_VER}

echo "-----------------"
echo "Setting up environment for PyROOT (ROOT in Python 3)."
echo " - ROOT_VER: ${ROOT_VER}"
echo " - ROOT_DIR: ${ROOT_DIR}"

echo " - Setting PATH..."
export PATH=${ROOT_DIR}/bin:$PATH

echo " - Setting PYTHONPATH..."
export PYTHONPATH=${ROOT_DIR}/lib

echo " - Setting LD_LIBRARY_PATH..."
export LD_LIBRARY_PATH=${ROOT_DIR}/lib

echo "Setup complete!"
echo "-----------------"
echo "You may now use PyROOT (ROOT in Python 3)!"
echo "You may test your environment using these commands:"
echo "  which root"
echo "  root --version"
echo "  python3"
echo "  >>> import ROOT"
echo "  >>> quit()"
echo "-----------------"

