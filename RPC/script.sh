#!/bin/bash

array=()

for file in ./logs/log*
do 
   while read line
   do 
       ip=$(echo "$line" | cut -d "," -f 2)
       if [[ ! ${array[@]} =~ $ip ]]
       then
           array+="$ip "
       fi
   done < "$file"
done

echo ${array[@]}