# run with bash ./install_conda_packages.sh
#  Original solution via StackOverflow:
#    http://stackoverflow.com/questions/35802939/install-only-available-packages-using-conda-install-yes-file-requirements-t
#

# option 1:
#  Install via `conda` directly.
#  This will fail to install all
#  dependencies. If one fails,
#  all dependencies will fail to install.
#
# conda install --yes --file requirements.txt

#
#  To go around issue above, one can
#  iterate over all lines in the
#  requirements.txt file.
#

# option 2
# install via conda only
# while read requirement; do conda install --yes $requirement; done < requirements.txt

# option 3
# install via conda, but if not there install via pip
while read requirement; do conda install --yes $requirement || pip install $requirement; done < requirements.txt