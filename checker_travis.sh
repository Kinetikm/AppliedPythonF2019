function check_python_code(){
 py.test --pep8 && pytest
}

function check_branch_name(){
 IFS=', ' read -r -a branch_data <<< "$(git show -s --pretty=%d HEAD | tr -d '()')"
 echo "$(git show -s --pretty=%d HEAD)"
 echo "${branch_data[0]}"
 echo "${branch_data[1]}"
 if [ "$1" != "${branch_data[2]}" ]; then
   echo "Bad branch name your value: ${branch_data[2]}, asked: $1}"
   exit 1
 fi
 if [ "origin/${branch_data[2]}" != "${branch_data[1]}" ]; then
   echo "Bad pull request, should be from origin/$1 not from ${branch_data[1]}"
   exit 1
 fi
}

args=("$@")
echo $# arguments passed
if [[ $# -lt 1 ]]; then
   exit 1
fi

check_branch_name "${args[0]}"
check_python_code