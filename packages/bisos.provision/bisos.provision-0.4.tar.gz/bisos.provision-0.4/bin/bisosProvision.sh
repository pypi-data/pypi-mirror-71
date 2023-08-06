#!/bin/bash

IcmBriefDescription="BISOS Provisioning -- Create the needed framework for BISOS."

####+BEGINNOT: bx:dblock:global:file-insert :file "/opt/idaas/gitRepos/idaas/idaas/tools/common/lib/bash/mainRepoRootDetermine.bash"
#
# DO NOT EDIT THIS SECTION (dblock)

# 

scriptSrcRunBase="$( dirname ${BASH_SOURCE[0]} )"
icmPkgRunBase=$(readlink -f ${scriptSrcRunBase}) 
icmSeedFile="${icmPkgRunBase}/seedIcmStandalone.bash"

if [ "${loadFiles}" == "" ] ; then
    "${icmSeedFile}" -l $0 "$@" 
    exit $?
fi

####+END:

# /opt/bisosProvisioner/gitRepos/provisioners/bin/bisosProvisioners_lib.sh
if [ -f /opt/bisosProvisioner/gitRepos/provisioners/bin/bisosProvisioners_lib.sh ] ; then
    . /opt/bisosProvisioner/gitRepos/provisioners/bin/bisosProvisioners_lib.sh
fi


#mainRepoRoot=$( cd $(dirname $0); git rev-parse --show-toplevel 2> /dev/null )

rootBase="/opt"
beSilent="false"

provisionerBase="${rootBase}/bisosProvisioner"

    # local currentUser=$(id -un)
    # local currentUserGroup=$(id -g -n ${currentUser})


    # local bx_platformInfoManage=$( which -a bx-platformInfoManage.py | grep -v venv | head -1 )

    # if [ ! -f "${bx_platformInfoManage}" ] ; then 
    # 	echoErr "Missing ${bx_platformInfoManage}"
    # 	return 1
    # fi
    
    # local bisosUserName=$( ${bx_platformInfoManage} -i pkgInfoParsGet | grep bisosUserName | cut -d '=' -f 2 )
    # local bisosGroupName=$( ${bx_platformInfoManage}  -i pkgInfoParsGet | grep bisosGroupName | cut -d '=' -f 2 )
    
    # local rootDir_bisos=$( ${bx_platformInfoManage}  -i pkgInfoParsGet | grep rootDir_bisos | cut -d '=' -f 2 )
    # local rootDir_bxo=$( ${bx_platformInfoManage}  -i pkgInfoParsGet | grep rootDir_bxo | cut -d '=' -f 2 )
    # local rootDir_deRun=$( ${bx_platformInfoManage} -i pkgInfoParsGet | grep rootDir_deRun | cut -d '=' -f 2 )        

      
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
$( examplesSeperatorChapter "BISOS Provisioning:: Standalone ICM Sets Up Selfcontained ICMs" )
$( examplesSeperatorSection "Create bisosProvision base directories" )
${G_myName} ${extraInfo} -i gitBinsPrep
${G_myName} ${extraInfo} -i gitPrep
${G_myName} ${extraInfo} -p rootBase=/opt -i provisionerRepoClone
${G_myName} ${extraInfo} -p rootBase=/opt -i provisionerBasesPrep
${G_myName} ${extraInfo} -i provisionerRepoClone
${G_myName} ${extraInfo} -i provisionerBasesPrep
_EOF_
    if [ -f /opt/bisosProvisioner/gitRepos/provisioners/bin/bisosProvisioners_lib.sh ] ; then
	vis_provisionersExamples "${extraInfo}"
    fi
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

    local currentUser=$(id -nu)
    local currentGroup=$(id -ng)
    
    lpDo sudo  mkdir -p "${provisionerBase}"

    lpDo sudo chown ${currentUser}:${currentGroup} "${provisionerBase}"

    local gitReposAnonBase="${provisionerBase}/gitReposAnon"
    local gitReposBase="${provisionerBase}/gitRepos"    
    
    lpDo mkdir -p "${gitReposAnonBase}"
    
    inBaseDirDo "${gitReposAnonBase}" git clone https://github.com/bxGenesis/provisioners.git

    lpDo mkdir -p "${gitReposBase}"

    lpDo ln -s "${gitReposAnonBase}/provisioners" "${gitReposBase}"
    
    lpReturn
}


function vis_provisionerBasesPrep {
    G_funcEntry
    function describeF {  G_funcEntryShow; cat  << _EOF_
_EOF_
    }
    EH_assert [[ $# -eq 0 ]]

    modulePrep

    # /opt/bisosProvisioner/gitRepos/provisioners
    local provisionersBase="${provisionerBase}/gitRepos/provisioners"

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


function vis_updateAcctsNOT {
    G_funcEntry
    function describeF {  G_funcEntryShow; cat  << _EOF_
_EOF_
    }
    EH_assert [[ $# -eq 0 ]]

    opDo provisionersPrep

    # /opt/bisosProvisioner}/gitRepos/provisioners/bin/bisosAccounts.sh
    local bisosAccountsProg="${provisionerBase}/gitRepos/provisioners/bin/bisosAccounts.sh"
    opDo vis_provisionerBasesPrep    

    if [ ! -x "${bisosAccountsProg}" ] ; then
	EH_problem "Missing ${bisosAccountsProg}"
	lpReturn 1
    else	
    	opDo "${bisosAccountsProg}" -h -v -n showRun -i fullUpdate passwd_tmpSame
    fi
    
    lpReturn
}

function vis_pythonSysEnvPrepForVirtenvsNO {
    G_funcEntry
    function describeF {  G_funcEntryShow; cat  << _EOF_
_EOF_
    }
    EH_assert [[ $# -eq 0 ]]

    opDo provisionersPrep

    # /opt/bisosProvisioner}/gitRepos/provisioners/bin/bisosBaseDirsSetup.sh
    local bisosProg="${provisionerBase}/gitRepos/provisioners/bin/bisosBaseDirsSetup.sh"

    if [ ! -x "${bisosProg}" ] ; then
	EH_problem "Missing ${bisosProg}"
	lpReturn 1
    else	
    	opDo "${bisosProg}" -h -v -n showRun -i pythonSysEnvPrepForVirtenvs
    fi
    
    lpReturn
}


function vis_bisosBaseDirsSetupNOT {
    G_funcEntry
    function describeF {  G_funcEntryShow; cat  << _EOF_
_EOF_
    }
    EH_assert [[ $# -eq 0 ]]

    opDo provisionersPrep

    # /opt/bisosProvisioner}/gitRepos/provisioners/bin/bisosBaseDirsSetup.sh
    local bisosProg="${provisionerBase}/gitRepos/provisioners/bin/bisosBaseDirsSetup.sh"

    if [ ! -x "${bisosProg}" ] ; then
	EH_problem "Missing ${bisosProg}"
	lpReturn 1
    else	
    	opDo "${bisosProg}" -h -v -n showRun -i bisosBaseDirsSetup
    fi
    
    lpReturn
}
