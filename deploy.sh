#!/bin/bash
# Author: tongphe.org@gmail.com
# Description: a script using git to deploy product

PROJECT_PATH=""
PROJECT_URL=""
BRANCH=""
REVERT_COMMIT=""

ORIGIN='origin'
RELEASE='releases'
CURRENT='current'
LAST_VERSION='last_version'
DEPLOY_INFO='false'
KEEP_VERSION=5
LOG_POSTFIX='.log'
DEPLOY_TIME=$(date "+%d-%m-%y %H:%M")
LOAD_VERSION=-1

function deploy_product() {
    git_clone
    deploy_release
    current_info
}

function git_clone() { 
    cd $PROJECT_PATH
    if [ ! -d $RELEASE ]; then
        mkdir $RELEASE
    fi

    if [ -d $ORIGIN ]; then
        rm -rf $ORIGIN
    fi
    # Clone repo
    git clone -b $BRANCH $PROJECT_URL $ORIGIN >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "Error git clone"
        exit 1
    fi
    echo "Cloning branch '$BRANCH'..."
    cd $ORIGIN
    git checkout $BRANCH
    echo "Finish cloning."
}

function deploy_release() {
    cd $PROJECT_PATH
    echo "Preparing to deploy..."
    last_version=$(cat $LAST_VERSION 2>/dev/null)
    if [ $? -ne 0 ]; then
        last_version=0
    fi
    last_version=$((last_version + 1))

    # Log deploy info
    deploy_log="$PROJECT_PATH/$RELEASE/$last_version$LOG_POSTFIX"
    echo "Deploy time: $DEPLOY_TIME" >> $deploy_log 
    echo "Deploy commit:" >> $deploy_log 
    cd $ORIGIN
    git log -1 >> $deploy_log
    cd ..

    # Deploy new source code
    rm -rf "$ORIGIN/.git"
    mv $ORIGIN "$RELEASE/$last_version"
    if [ $? -ne 0 ]; then
        echo "Error deploy version"
        exit 1
    fi
    unlink $CURRENT 2>/dev/null
    ln -s "$RELEASE/$last_version" $CURRENT
    if [ $? -ne 0 ]; then
        echo "Error switch version"
        exit 1
    fi
    echo $last_version > $LAST_VERSION 

    # Remove old version
    old_version="$RELEASE/$((last_version - KEEP_VERSION))"
    if [ -d $old_version ]; then
        rm -rf $old_version
    fi
    old_version_log="$old_version$LOG_POSTFIX"
    if [ -f $old_version_log ]; then
        rm $old_version_log 
    fi

    echo "Successfully deployed."
}

function git_revert() { 
    if [ "$REVERT_COMMIT" == "" ]; then
        echo "Error revert commit is not valid"
        exit 1
    fi
    git_clone
    cd "$PROJECT_PATH/$ORIGIN"
    git checkout $BRANCH >/dev/null 2>&1
    git checkout $REVERT_COMMIT >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "Error revert commit $REVERT_COMMIT failed"
        exit 1
    fi
    git clean -f
    deploy_release
    echo "Successfully revert commit to $REVERT_COMMIT."
    current_info
}

function switch_back() {
    version_back=$1
    cd $PROJECT_PATH
    last_version=$(cat $LAST_VERSION)
    current_version=$(basename $( ls -l $CURRENT | awk '{print $NF}'))
    if [ $version_back -ge $KEEP_VERSION ]; then
        echo "Error revert version too far"
        exit 1
    fi
    revert_version=$((last_version - version_back))
    if [ $current_version -eq $revert_version ]; then
        echo "Error already on version $revert_version"
        exit 1
    fi
    if [ ! -d "$RELEASE/$revert_version" ]; then
        echo "Error version doesn't exist"
        exit 1
    fi

    unlink $CURRENT 2>/dev/null
    ln -s "$RELEASE/$((last_version - version_back))" $CURRENT
    if [ $? -ne 0 ]; then
        echo "Error switch version"
        exit 1
    fi

    echo "Successfully switch $version_back version."
    current_info
}

function current_info() {
    cd $PROJECT_PATH
    current_version=$(basename $( ls -l $CURRENT | awk '{print $NF}'))
    echo "Current version: $current_version"
    echo "Latest version: $(cat $LAST_VERSION)"
    current_log="$RELEASE/$current_version$LOG_POSTFIX"
    if [ -f $current_log ]; then
        echo "----------------------------------------"
        echo "Version $current_version:"
        cat $current_log
    fi
}

function deploy_info() {
    current_info 
    last_version=$(cat $LAST_VERSION)
    cd $PROJECT_PATH
    echo "Last $KEEP_VERSION versions infomations:"
    for ((version=last_version;version>last_version-KEEP_VERSION;version--)); do
        log_version="$RELEASE/$version$LOG_POSTFIX"
        if [ -f $log_version ]; then
            echo "----------------------------------------"
            echo "Version $version:"
            cat $log_version
        fi
    done
}

function check_settings() {
    local miss=""

    if [ "$PROJECT_PATH" == "" ]; then
        miss="project_path"
    fi

    if [ "$PROJECT_URL" == "" ]; then
        miss="$miss, project_url"
    fi

    if [ "$BRANCH" == "" ]; then
        miss="$miss, branch"
    fi
    echo $miss
}

function check_requirement() {
    local miss=""

    for depend in $*; do
        if [ ! $(command -v $depend) ]; then
            miss="$miss, $depend"
        fi
    done
    echo $miss
}

function init_settings() {
    # Check settings
    err_opt=$(check_settings)
    if [ "$err_opt" != "" ]; then
        echo "Error missing options: $err_opt"
        exit 1
    fi

    # Check requirement and tool
    err_req=$(check_requirement git)
    if [ "$err_req" != "" ]; then
        echo "Error requirement: $err_req"
        exit 1
    fi

    # Check project path write permission
    if [ ! -d $PROJECT_PATH ]; then
        mkdir -p $PROJECT_PATH
        if [ $? -ne 0 ]; then
            echo "Error project directory write permission"
            exit 1
        fi
    elif [ ! -w $PROJECT_PATH ]; then
        echo "Error project directory write permission"
        exit 1
    fi
}

function main() {
    # Deploy or Revert product
    if [ "$DEPLOY_INFO" == "true" ]; then
        deploy_info
        exit 0
    fi
    
    if [ $LOAD_VERSION -gt -1 ]; then
        switch_back $LOAD_VERSION
        exit 0
    fi

    if [ "$REVERT_COMMIT" == "" ]; then
        deploy_product
        exit 0
    else
        git_revert
        exit 0
    fi
}

# Init deploy options
while getopts "p:u:b:r:l:t:i-" opt; do
    case $opt in
        p)
            PROJECT_PATH="$OPTARG";;
        u)
            PROJECT_URL="$OPTARG";;
        b)
            BRANCH="$OPTARG";;
        r)
            REVERT_COMMIT="$OPTARG";;
        l)
            LOAD_VERSION=$OPTARG;;
        i)
            DEPLOY_INFO='true';;
        t)
            DEPLOY_TIME="$OPTARG";;
        -)
            echo "Type '$(basename "$0") --help' for more information."
            exit 1;;
        \?)
            echo "Type '$(basename "$0") --help' for more information."
            exit 1;;
    esac
done

shift $(($OPTIND - 1))

init_settings
lock_file="$PROJECT_PATH/deploy.lock"
(
    flock -n 200
    if [ $? -ne 0 ]; then
        echo "Error other deploy process for this project is running" 
        exit 1
    fi
    main
) 200>$lock_file
rm $lock_file
