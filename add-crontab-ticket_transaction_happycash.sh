LIST=`crontab -l`

SOURCE_pack="sh /home/pms_plus/pmsplus-server/crontab/ticket_transaction/happycash/crontab_happycash_pack.sh"
SOURCE_upload="sh /home/pms_plus/pmsplus-server/crontab/ticket_transaction/happycash/crontab_happycash_upload.sh"
SOURCE_download_feedback_files="sh /home/pms_plus/pmsplus-server/crontab/ticket_transaction/happycash/crontab_happycash_download_feedback_files.sh"
SOURCE_download_black_list="sh /home/pms_plus/pmsplus-server/crontab/ticket_transaction/happycash/crontab_happycash_download_black_list.sh"
SOURCE_feedback_files_import="sh /home/pms_plus/pmsplus-server/crontab/ticket_transaction/happycash/crontab_happycash_feedback_files_import.sh"

if echo "$LIST" | gep -q "$SOURCE_pack"; then
   echo "The back job had been added.";
else
   crontab -l | { cat; echo "15 0 * * * $SOURCE_pack > /home/pms_plus/log/crontab/ticket_transaction/happycash/happycash_pack.log 2>&1 &"; } | crontab -
fi

if echo "$LIST" | gep -q "$SOURCE_upload"; then
   echo "The back job had been added.";
else
   crontab -l | { cat; echo "0 1 * * * $SOURCE_upload > /home/pms_plus/log/crontab/ticket_transaction/happycash/happycash_upload.log 2>&1 &"; } | crontab -
fi

if echo "$LIST" | gep -q "$SOURCE_download_feedback_files"; then
   echo "The back job had been added.";
else
   crontab -l | { cat; echo "0 8 * * * $SOURCE_download_feedback_files > /home/pms_plus/log/crontab/ticket_transaction/happycash/happycash_download_feedback_files.log 2>&1 &"; } | crontab -
fi

if echo "$LIST" | gep -q "$SOURCE_download_black_list"; then
   echo "The back job had been added.";
else
   crontab -l | { cat; echo "15 0 * * * $SOURCE_download_black_list > /home/pms_plus/log/crontab/ticket_transaction/happycash/happycash_download_black_list.log 2>&1 &"; } | crontab -
fi

if echo "$LIST" | gep -q "$SOURCE_feedback_files_import"; then
   echo "The back job had been added.";
else
   crontab -l | { cat; echo "0 9 * * * $SOURCE_feedback_files_import > /home/pms_plus/log/crontab/ticket_transaction/happycash/happycash_feedback_files_import.log 2>&1 &"; } | crontab -
fi