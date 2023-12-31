#!/bin/sh

die () {
   echo "*** mkconfig.sh: $*" 1>&2
   exit 1
}

[ -f makefile ] || die "can not find 'makefile'"

sed \
  -e '/^C[A-Z]*=/!d' \
  -e 's,^,#define PICOSAT_,' \
  -e 's,= *, ",' \
  -e 's,$,",' \
  makefile

id=""
if [ -d .git -a -f .git/HEAD ]
then
  head="`awk 'NF == 1' .git/HEAD`"
  if [ x"$head" = x ]
  then
    head="`awk '{print $2}' .git/HEAD`"
    if [ ! x"$head" = x -a -f ".git/$head" ]
    then
      id=" `cat .git/$head`"
    fi
  else
    id=" $head"
  fi
fi

echo "#define PICOSAT_VERSION \"`cat VERSION`$id\""

exit 0
