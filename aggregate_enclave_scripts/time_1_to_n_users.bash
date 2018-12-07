#!/bin/bash

echo Start timestamp: `date +%s` >> times.txt

for j in `seq 1 5`;
do
	for i in `seq 1 10`;
	do

	    python3 create_new_user_data.py $((5 * $i))
            
	    start=`date +%s`
	    python3 send_agg_request.py
            end=`date +%s`
	    runtime=$((end-start))
	    echo i=$((5 * $i)) runtime: $runtime >> times.txt
	done
done

