#!/bin/sh
#  msg/wdimex.sh -- make generic message.wdm for libraries
#
# History:  95/12/05 kmflynn  clean up for tape 3
#           99/02/16 kmflynn
#
# Usage: wdimex.sh [file_name [parm_version]] [| tee output_file]
#
# Where: file_name = the name of the message file to build
#                    message - to generate generic message file (default)
#        parm_version is the version of the parm__.seq file
#                    dg - data general using prior-gks (default)
#                    xgks - unix using Xgks
#                    gli  - unix using gli
#                    pc - using interactor
#
# Examples:  wdimex.sh message gli
#
# Note:  the ___.in files are left in the direcory for the pc make, kmf

#*******************************************************************
#***** You should not need to modify anything below this line. *****
#*******************************************************************

Optn=${1-'message'}
     if [ ! $Optn ] ; then Optn=message ; fi
Vers=${2-'gli'}
     if [ ! $Vers ] ; then Vers=gli ; fi


binDir=../bin
LibDat=../lib_data

# system dependent sequential file
  Parm=aide/parm$Vers

# sequential files for generic message.wdm
  NameM=message
  SeqM='aide/message waide/awfeb waide/prwfil waide/atinfo'

  echo
  echo ' parm__.seq version:' parm$Vers.seq
  echo ' building wdm files:' $Optn
  echo
  if [ $Optn = 'message'  -o  $Optn = 'both' ]
    then
#   build the generic message file
    echo
    echo ' building the generic message file' $NameM'.wdm'
    echo
  
#   remove any old files
    if [ -f error.fil ]          ; then rm error.fil          ; fi
    if [ -f $NameM.in ]          ; then rm $NameM.in          ; fi
    if [ -f $NameM.wdm ]         ; then rm $NameM.wdm         ; fi
    if [ -f $LibDat/$NameM.wdm ] ; then rm $LibDat/$NameM.wdm ; fi
  
#   build input file
    echo $NameM.wdm > $NameM.in
    echo C >> $NameM.in
    echo Y >> $NameM.in
    echo adwdm/ >> $NameM.in
    for Seq in $SeqM $Parm ; do
       echo I >> $NameM.in
       echo $Seq.seq >> $NameM.in
    done
    echo R >> $NameM.in
  
#   build message file
    $binDir/wdimex < $NameM.in

#   move new message file and clean up files
    mv $NameM.wdm $LibDat/$NameM.wdm

  fi

# end of shell
