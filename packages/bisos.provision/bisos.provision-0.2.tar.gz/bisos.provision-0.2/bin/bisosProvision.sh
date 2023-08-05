#!/bin/bash

IcmBriefDescription="BISOS Provisioning -- Create the needed framework for BISOS."

####+BEGINNOT: bx:dblock:global:file-insert :file "/opt/idaas/gitRepos/idaas/idaas/tools/common/lib/bash/mainRepoRootDetermine.bash"
#
# DO NOT EDIT THIS SECTION (dblock)
# /opt/idaas/gitRepos/idaas/idaas/tools/common/lib/bash/mainRepoRootDetermine.bash common dblock inserted code
#

gitTopLevelOffset="ci-actions"   # Specified as a dblock parameter
specifiedIcmPkgRunBase="/opt/idaas/gitRepos/idaas/ci-actions" # Specified as a dblock parameter
scriptSrcRunBase="$( dirname ${BASH_SOURCE[0]} )"
icmPkgRunBase=$(readlink -f ${scriptSrcRunBase}/..)  # Assuming Packaged ICM in bin
icmSeedFile="${icmPkgRunBase}/bin/seedIcmStandalone.bash"

if [ ! -f "${icmSeedFile}" ] ; then
    #echo "Assuming Detatched ICM Inside Of A Git Repo"
    mainRepoRoot=$( cd ${scriptSrcRunBase} ;  git rev-parse --show-toplevel 2> /dev/null )
    if [ ! -z "${mainRepoRoot}" ] ; then
	icmSeedFile="${mainRepoRoot}/${gitTopLevelOffset}/bin/seedIcmStandalone.bash"
	if [ -f "${icmSeedFile}" ] ; then 	
	    icmSeedFile="${icmSeedFile}"  # opDoNothing
	fi
    else
	icmPkgRunBase="${specifiedIcmPkgRunBase}"
	icmSeedFile="${icmPkgRunBase}/bin/seedIcmStandalone.bash"
	if [ ! -f "${icmSeedFile}" ] ; then 
	    echo "E: Missing ${icmSeedFile} -- Misconfigured icmPkgRunBase"
	    exit 1
	fi
    fi
fi
if [ "${loadFiles}" == "" ] ; then
    "${icmSeedFile}" -l $0 "$@" 
    exit $?
fi

####+END:

#mainRepoRoot=$( cd $(dirname $0); git rev-parse --show-toplevel 2> /dev/null )

rootBase="/opt"
beSilent="false"

provisionerBase="${rootBase}/bisosProvisioner"
      
genesisGitRepoCloneCmnd="git clone https://github.com/bxGenesis/provisioners.git"


function vis_describe {  cat  << _EOF_
BISOS Provisioer is a minimal standaloneIcm that creates a standaloneIcmEnv
and invokes facilities there.
_EOF_
		      }

# Import Libraries


function G_postParamHook {
     return 0
}

function vis_examples {
    typeset extraInfo="-h -v -n showRun"
    #typeset extraInfo=""
    typeset runInfo="-p ri=lsipusr:passive"

    typeset examplesInfo="${extraInfo} ${runInfo}"

    visLibExamplesOutput ${G_myName} 
  cat  << _EOF_
$( examplesSeperatorTopLabel "${G_myName}" )
$( examplesSeperatorChapter "BISOS Provisioning" )
$( examplesSeperatorSection "Create bisosProvision base directories" )
${G_myName} ${extraInfo} -i gitBinsPrep
${G_myName} ${extraInfo} -i gitPrep
${G_myName} ${extraInfo} -p rootBase=/opt -i provisionerRepoClone
${G_myName} ${extraInfo} -p rootBase=/opt -i provisionerBasesPrep
${G_myName} ${extraInfo} -i provisionerRepoClone
${G_myName} ${extraInfo} -i provisionerBasesPrep
$( examplesSeperatorSection "Create Accounts" )
${G_myName} ${extraInfo} -i updateAccts
$( examplesSeperatorSection "Create BisosProv Virtenvs" )
${G_myName} ${extraInfo} -i pythonSysEnvPrepForVirtenvs
$( examplesSeperatorSection "Create /bisos Bases" )
${G_myName} ${extraInfo} -i bisosBaseDirsSetup
_EOF_
}

noArgsHook() {
  vis_examples
}

function modulePrep {
    G_funcEntry
    function describeF {  G_funcEntryShow; cat  << _EOF_
_EOF_
    }
    EH_assert [[ $# -eq 0 ]]

    provisionerBase="${rootBase}/bisosProvisioner"
    
    lpReturn
}


function vis_gitBinsPrep {
    G_funcEntry
    function describeF {  G_funcEntryShow; cat  << _EOF_
_EOF_
    }
    EH_assert [[ $# -eq 0 ]]

    opDo sudo apt-get update
    opDo sudo apt-get -y install git      

    lpReturn
}


function vis_gitPrep {
    G_funcEntry
    function describeF {  G_funcEntryShow; cat  << _EOF_
_EOF_
    }
    EH_assert [[ $# -eq 0 ]]

    #opDo sudo git init

    lpReturn
}



function vis_provisionerRepoClone {
    G_funcEntry
    function describeF {  G_funcEntryShow; cat  << _EOF_
_EOF_
    }
    EH_assert [[ $# -eq 0 ]]

    opDo modulePrep

    local gitReposBase="$provisionerBase}/gitRepos"
    
    opDo sudo  mkdir -p "${gitReposBase}"

    inBaseDirDo "${gitReposBase}" sudo git clone https://github.com/bxGenesis/provisioners.git
    
    lpReturn
}


function vis_provisionerBasesPrep {
    G_funcEntry
    function describeF {  G_funcEntryShow; cat  << _EOF_
_EOF_
    }
    EH_assert [[ $# -eq 0 ]]

    modulePrep

    # /opt/bisosProvisioner}/gitRepos/provisioners
    local provisionersBase="$provisionerBase}/gitRepos/provisioners"

    if [ -d "${provisionersBase}" ] ; then
	if [ "${beSilent}" != "true" ] ; then  
	    ANT_raw "${provisionersBase} is in place, preparation skipped"
	fi
    else	
    
	opDo vis_gitBinsPrep

	opDo vis_gitPrep

	opDo vis_provisionerRepoClone
    fi
    
    lpReturn
}

function provisionersPrep {
    G_funcEntry
    function describeF {  G_funcEntryShow; cat  << _EOF_
_EOF_
    }
    EH_assert [[ $# -eq 0 ]]

    modulePrep
    
    beSilent="true"
    
    lpReturn
}


function vis_updateAccts {
    G_funcEntry
    function describeF {  G_funcEntryShow; cat  << _EOF_
_EOF_
    }
    EH_assert [[ $# -eq 0 ]]

    opDo provisionersPrep

    # /opt/bisosProvisioner}/gitRepos/provisioners/bin/bisosAccounts.sh
    local bisosAccountsProg="$provisionerBase}/gitRepos/provisioners/bin/bisosAccounts.sh"
    opDo vis_provisionerBasesPrep    

    if [ ! -x "${bisosAccountsProg}" ] ; then
	EH_problem "Missing ${bisosAccountsProg}"
	lpReturn 1
    else	
    	opDo "${bisosAccountsProg}" -h -v -n showRun -i fullUpdate passwd_tmpSame
    fi
    
    lpReturn
}

function vis_pythonSysEnvPrepForVirtenvs {
    G_funcEntry
    function describeF {  G_funcEntryShow; cat  << _EOF_
_EOF_
    }
    EH_assert [[ $# -eq 0 ]]

    opDo provisionersPrep

    # /opt/bisosProvisioner}/gitRepos/provisioners/bin/bisosBaseDirsSetup.sh
    local bisosProg="$provisionerBase}/gitRepos/provisioners/bin/bisosBaseDirsSetup.sh"

    if [ ! -x "${bisosProg}" ] ; then
	EH_problem "Missing ${bisosProg}"
	lpReturn 1
    else	
    	opDo "${bisosProg}" -h -v -n showRun -i pythonSysEnvPrepForVirtenvs
    fi
    
    lpReturn
}


function vis_bisosBaseDirsSetup {
    G_funcEntry
    function describeF {  G_funcEntryShow; cat  << _EOF_
_EOF_
    }
    EH_assert [[ $# -eq 0 ]]

    opDo provisionersPrep

    # /opt/bisosProvisioner}/gitRepos/provisioners/bin/bisosBaseDirsSetup.sh
    local bisosProg="$provisionerBase}/gitRepos/provisioners/bin/bisosBaseDirsSetup.sh"

    if [ ! -x "${bisosProg}" ] ; then
	EH_problem "Missing ${bisosProg}"
	lpReturn 1
    else	
    	opDo "${bisosProg}" -h -v -n showRun -i bisosBaseDirsSetup
    fi
    
    lpReturn
}
