wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1AgxnWx4NXiA1yR_sDdyJkngVSeUchwaV' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1AgxnWx4NXiA1yR_sDdyJkngVSeUchwaV" -O GraphV_DB.zip && rm -rf /tmp/cookies.txt &&\
unzip GraphV_DB.zip &&\
rm  GraphV_DB.zip

