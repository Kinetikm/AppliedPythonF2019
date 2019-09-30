function check_python_code(){
 py.test --pep8 && pytest
}

function check_branch_name(){
 echo "$TRAVIS_PULL_REQUEST"
 printenv
 exit 1
}

args=("$@")
echo $# arguments passed
if [[ $# -lt 1 ]]; then
   exit 1
fi

check_branch_name "${args[0]}"
check_python_code