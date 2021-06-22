#!/bin/bash 
########################################################################
#
# Name          : install.sh
# Purpose       : ancillary functions to install the different project modules
# Arguments     : N/A
#
# History       :       
#
# Created       : Aug 2020
########################################################################

# Defining some Maven plugins
maven_dep_cp_plugin=org.apache.maven.plugins:maven-dependency-plugin:3.0.1:copy
maven_exec_plugin=org.codehaus.mojo:exec-maven-plugin:1.3.1:exec

########################################
## Get property from any property file
# arg 1: file properties absolute path
# arg 2: property name
########################################
function get_property {
    grep "^$2=" "$1" | cut -d'=' -f2
}

########################################
## Get property from pom.xml
# arg 1: pom.xml absolute path
# arg 2: property name
########################################
function get_pom_property {    
    mvn -f $1 -q -Dexec.executable="echo" -Dexec.args=$2 --non-recursive $maven_exec_plugin
}

########################################
## Create a tmp dir in case it does not exist
# arg 1: dir absolute path
########################################
function create_temporary_dir {    
   if [ ! -d "$1" ]; then
      mkdir $1
   else
      if [ "$(ls -A $1)" ]; then
        echo "Removing files of $1"
        rm $1/*
      fi
   fi
}

########################################
## remote a tmp dir in case it does  exist
# arg 1: dir absolute path
########################################
function remove_temporary_dir {    
   if [ -d "$1" ]; then
     echo "Removing temporary dir $1";
     rm -rf $1;
   fi
}

########################################
## Retrieves a specific artifact from nexus
# arg 1: pom.xml absolute path
# arg 2: artifact to download
# arg 3: outputDirectory
########################################
function download_package_from_nexus {   
  echo "Downloading $2 from Nexus..."
  mvn -f $1 $maven_dep_cp_plugin -Dartifact=$2 -DoutputDirectory=$3
}

########################################
## Copies a package (war/tar..) to a remote server
# arg 1: file to copy
# arg 2: remote path
########################################
function copy_package_to_remote_server {    
  if [ ! -f $1 ]; then
    echo "====> $1 does not exist, installation stops!";
    exit
  fi

  echo "Copying remotely file $1 to $2..."
  scp $1 $2 
}

########################################
## Copies a package (war/tar..) to a local server
# arg 1: file to copy
# arg 2: destination path
########################################
function copy_package_to_local_server {    
  if [ ! -f $1 ]; then
    echo "====> $1 does not exist, installation stops!";
    exit
  fi

  echo "Copying package file $1 to $2..."
  cp $1 $2 
}

########################################
## Retrieves identifiers for the SW package
# of the package to copy remotely
# arg 1: pom path
# arg 2: artifact
# arg 3: artifact_name
# arg 4: artifact_dir
# arg 5: artifact_id
# arg 6: overwrite_version ('-' do not override)
# arg 7: overwrite_packaging ('-' do not override)
########################################
function obtain_package_details {    
  echo "Getting project coordinates from pom.xml...";
  groupId=`get_pom_property $1 '${project.groupId}'`;
  artifactId=`get_pom_property $1 '${project.artifactId}'`;
  
  # Version
  if [ "$6" != "-" ]; then
    version=$6
  else
    version=`get_pom_property $1 '${project.version}'`;
  fi
  
  # Packaging
  if [ "$7" != "-" ]; then
    packaging=$7
  else
    packaging=`get_pom_property $1 '${project.packaging}'`;
  fi

  # Putting all together
  eval $2="$groupId:$artifactId:$version:$packaging"
  eval $3="$artifactId-$version.$packaging"
  eval $4="$artifactId-$version"
  eval $5="$artifactId"
}

########################################
## Retrieves from the properties file the remote dir to install the package
# of the package to copy remotely
# arg 1: properties file path
# arg 2: server_user
# arg 3: server_host
# arg 4: server_instdir
# arg 5: remote_dir
########################################
function retrieve_remote_package_location {    
  eval $2=`get_property $1 server.user`;
  eval $3=`get_property $1 server.host`;
  eval $4=`get_property $1 server.instdir`;

  eval $5="$server_user@$server_host:$server_instdir/"
}

########################################
## Perform several actions for the tar packages in the remote server
# of the package to copy remotely
# arg 1: server_user
# arg 2: server_host
# arg 3: server_instdir
# arg 4: artifact_dir
# arg 5: artifact_name
# arg 6: artifact_id
########################################
function remote_actions_tar_packages {    
ssh "$1@$2" "
  echo "  cd $3";
  cd $3;
  
  if [ -e $4 ] ; then mv $4 /tmp/$4.old.`date +%y%m%d_%H%M%S`;  fi
  echo "  creating directory $4...";
  mkdir $4;
  
  echo "  untar tar $5...";
  if [ -e $5 ] ; then tar xf $5 -C $4;  fi
  
  echo "  remove tar $5...";
  rm -rf $5; 
  
  echo "  change bin permissions of $4/bin/ ...";
  chmod 744 $4/bin/**;
"
}

function update_db_passwd() {
    remote_command="ssh geaops@esdcconf.n1data.lan /home/geaops/passw/getprop spring.datasource.password"
	echo "Remote command: $remote_command"
	output=$($remote_command)
	echo "Output: $output"
	if [ -z "$output" ]; then
		echo
		echo "ERROR: No value for property 'spring.datasource.password' in properties host: $PROPERTIES_SERVER_HOST"
		echo
		exit
	fi
	
	cmd="sed -i -e 's/^\(spring.datasource.password\s*=\s*\).*\$/\1$output/' BOOT-INF/classes/application.properties"
    eval $cmd
}



