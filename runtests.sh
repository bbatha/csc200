#!/usr/bin/env zsh

total=0
pass=0
percentage=0
nops=0
out=output.log
size=`wc -c a.out | awk '{print $1}'`

echo "Potentially changing $size operations"
for ((i = 0; i < $size; i++)); do
    if [ `xxd -l 1 -s ${i} -ps a.out` = "00" ] ; then
        let "nops = nops + 1"
    elif [ `xxd -l 1 -s ${i} -ps a.out` = "" ] ; then
        echo "done at $i"
    else
        let "total = total + 1"
        cp a.out executables/$i.out
        printf '\xFF' | dd of=executables/$i.out bs=1 seek=$i count=3 conv=notrunc &>/dev/null
    fi
done

echo "${total} test executables were created in the executables folder."


#adapted from
#http://www.unix.com/shell-programming-scripting/160479-terminate-process-using-shell-script.html
unalias ls
for j in `ls executables`; do
    : >! $out
    echo "Testing executable ${j}..."
    unbuffer ./executables/$j >! $out &
    
    pid=$!
    sleep 5
    
    if ! kill -s 0 $pid; then
        echo "Failure -- linker"
    else
        kill $pid
        tail -f $out | while read line ; do
            echo $line | grep "1000000000" &>/dev/null
            if [ $? -eq 0 ] ; then
                tailPID=`ps ax | grep -v grep | grep "tail -f $out" | awk '{print $1}'`
                kill $tailPID
                let "pass = pass + 1"
                echo "Pass"
            else
                tailPID=`ps ax | grep -v grep | grep "tail -f $out" | awk '{print $1}'`
                kill $tailPID
                echo "Failue -- no output"
            fi
        done
    fi

done
let "percentage = pass * 1.0 / total"
echo "The clean executable has ${nops} nops and ${total} operations."
echo "${total} test executables were created in the executables folder."
echo "${pass} tests of ${total} passed (${percentage}%)"
