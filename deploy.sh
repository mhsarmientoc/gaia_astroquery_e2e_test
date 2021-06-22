#!/bin/bash

# Inherit from the parent
.  ./deploy_parent.sh

########################################################################
#
# Name          : deploy.sh
# Purpose       : deploy python wrapper
# Arguments     : enviroment
#
# History       :       
#
# Created       : Aug 2020
########################################################################

###########################
# defining some variables
###########################
baseDir="."
inst_dir="$baseDir/tmp_app_install"
properties_dir="$baseDir/config"
packaging="war"

# Environment may be overwritten with an input parameter
 if [ "$#" -gt  "0" ]; then
     environment=$1
     echo "Env: $environment"
 else
     environment="dev"
 fi
 
id="Gaia E2E Tests for Astroquery"

echo "=====> About to start installation of $id"

###############################
# 0.- Create temporary dir 
create_temporary_dir $inst_dir


###############################
# 1.- Create wheel package
version=`cat setup.py | grep version | grep -v description | awk 'BEGIN {FS="\x27"} {print $2}'`
wrapper=`python3 setup.py sdist bdist_wheel -P$environment | grep none-any | awk 'BEGIN {FS="\x27"} {print $2}'`
war_file=hreda-python-$version.war
notebook_demos=./build/demo/

echo "VERSION: $version"
echo "WRAPPER: $wrapper"
echo "NOTEBOOK: $notebook"
echo "WAR-FILE: $war_file"


###############################
# 2.- Copy package and jupiter_notebook demos into the temporary dir
cp $wrapper $inst_dir/.
cp $notebook_demos/* $inst_dir/.

##############################
# 3. - Create war file

cd $inst_dir
jar -cvf $war_file *

###############################
# 3.- Copy the artifact to the remote location
cd ..
properties_file=conf/${environment}.properties
file_path=$inst_dir/$war_file
retrieve_remote_package_location $properties_file server_user server_host server_instdir remotedir


 if [ "$environment" ==  "local" ]; then
     remotedir=$server_instdir/
     echo "Remote directory: $remotedir"
     copy_package_to_local_server $file_path $remotedir
 else
     remotedir="$server_user@$server_host:$server_instdir/"
     echo "Remote directory: $remotedir"
     copy_package_to_remote_server $file_path $remotedir
 fi


# 5. Cleanup and wrap
remove_temporary_dir $inst_dir
echo "<===== Installation finished of of $id"

