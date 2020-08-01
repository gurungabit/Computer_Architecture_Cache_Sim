size=(64 128)

block=(4 8 16 32 64)

assoc=(1 2 4 8 16)

for i in "${size[@]}"
do
   for j in "${block[@]}"
   do
      for k in "${assoc[@]}"
      do
        python cacheSim2.py -f Corruption2.trc -s $i -b $j -a $k -r RND >> sim3.cvs
      done
   done
done