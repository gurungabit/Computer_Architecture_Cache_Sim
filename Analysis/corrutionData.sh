size=(4 8 16 32 64 128 256 512 1024)

block=(4 8 16 32 64)

assoc=(1 2 4 8 16)

for i in "${size[@]}"
do
   for j in "${block[@]}"
   do
      for k in "${assoc[@]}"
      do
        echo python3 cacheSim2.py -f Corruption2.trc -s $i -b $j -a $k -r RR ">> sim.cvs" >> run.sh
      done
   done
done