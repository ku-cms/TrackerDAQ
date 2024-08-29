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

# Instructions from Alan Feltz (February 20, 2024):

# ROOT version installed to use PyROOT:
# root-6.30.04
export ROOT_VERSION="root-6.30.04"

echo "---------------"
echo "Setting up environment for PyROOT using ROOT (${ROOT_VERSION}) and Python 3."

echo "- Setting PATH..."
export PATH=/usr/local/root-6.30.04/bin:/usr/local/binutils-2.42/bin:/usr/local/gcc-13.2.0/bin:$PATH

echo "- Setting PYTHONPATH..."
export PYTHONPATH=/usr/local/root-6.30.04/lib

echo "- Setting LD_LIBRARY_PATH..."
export LD_LIBRARY_PATH=/usr/local/root-6.30.04/lib

echo "Setup complete!"
echo "---------------"
echo "You may now use PyROOT (ROOT in Python 3)."
echo "You may test your environment using these commands:"
echo "  which root"
echo "  python3"
echo "  >>> import ROOT"
echo "---------------"

