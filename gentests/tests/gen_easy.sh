for ((i = 5; i < 250; ++i))
do
	VERTICESCOUNT=$((i*50))
	EDGESCOUNT=$(($VERTICESCOUNT - 1))
#	MAXEDGESCOUNT=$(($VERTICESCOUNT * ($VERTICESCOUNT - 1) / 2 - 10))
#	if [ $MAXEDGESCOUNT -gt $EDGESCOUNT ]
#	then
#		EDGESCOUNT=$MAXEDGESCOUNT
#	fi
	python3 generator_easy.py $VERTICESCOUNT -e $EDGESCOUNT -s 0 -w 100 >> test_easy$((i - 5))
done
