LIST=`crontab -l`

SOURCE_pack="sh /home/pms_plus/pmsplus-server/crontab/ticket_transaction/ipass/crontab_ipass_pack.sh"
SOURCE_upload="sh /home/pms_plus/pmsplus-server/crontab/ticket_transaction/ipass/crontab_ipass_upload.sh"
SOURCE_download_feedback_files="sh /home/pms_plus/pmsplus-server/crontab/ticket_transaction/ipass/crontab_ipass_download_feedback_files.sh"
SOURCE_download_black_list_KBLI="sh /home/pms_plus/pmsplus-server/crontab/ticket_transaction/ipass/crontab_ipass_download_black_list_KBLI.sh"
SOURCE_download_black_list_KBLN="sh /home/pms_plus/pmsplus-server/crontab/ticket_transaction/ipass/crontab_ipass_download_black_list_KBLN.sh"
SOURCE_download_close_autoload_list="sh /home/pms_plus/pmsplus-server/crontab/ticket_transaction/ipass/crontab_ipass_download_close_autoload_list.sh"
SOURCE_feedback_files_import="sh /home/pms_plus/pmsplus-server/crontab/ticket_transaction/ipass/crontab_ipass_feedback_files_import.sh"

if echo "$LIST" | gep -q "$SOURCE_pack"; then
   echo "The back job had been added.";
else
   crontab -l | { cat; echo "15 0 * * * $SOURCE_pack > /home/pms_plus/log/crontab/ticket_transaction/ipass/ipass_pack.log 2>&1 &"; } | crontab -
fi

if echo "$LIST" | gep -q "$SOURCE_upload"; then
   echo "The back job had been added.";
else
   crontab -l | { cat; echo "0 1 * * * $SOURCE_upload > /home/pms_plus/log/crontab/ticket_transaction/ipass/ipass_upload.log 2>&1 &"; } | crontab -
fi

if echo "$LIST" | gep -q "$SOURCE_download_feedback_files"; then
   echo "The back job had been added.";
else
   crontab -l | { cat; echo "0 4 * * * $SOURCE_download_feedback_files > /home/pms_plus/log/crontab/ticket_transaction/ipass/ipass_download_feedback_files.log 2>&1 &"; } | crontab -
fi

if echo "$LIST" | gep -q "$SOURCE_download_black_list_KBLI"; then
   echo "The back job had been added.";
else
   crontab -l | { cat; echo "15 0,3,6,9,12,15,18,21 * * * $SOURCE_download_black_list_KBLI > /home/pms_plus/log/crontab/ticket_transaction/ipass/ipass_download_black_list_KBLI.log 2>&1 &"; } | crontab -
fi

if echo "$LIST" | gep -q "$SOURCE_download_black_list_KBLN"; then
   echo "The back job had been added.";
else
   crontab -l | { cat; echo "15 0 * * * $SOURCE_download_black_list_KBLN > /home/pms_plus/log/crontab/ticket_transaction/ipass/ipass_download_black_list_KBLN.log 2>&1 &"; } | crontab -
fi

if echo "$LIST" | gep -q "$SOURCE_download_close_autoload_list"; then
   echo "The back job had been added.";
else
   crontab -l | { cat; echo "15 0 * * * $SOURCE_download_close_autoload_list > /home/pms_plus/log/crontab/ticket_transaction/ipass/ipass_download_close_autoload_list.log 2>&1 &"; } | crontab -
fi

if echo "$LIST" | gep -q "$SOURCE_feedback_files_import"; then
   echo "The back job had been added.";
else
   crontab -l | { cat; echo "0 6 * * * $SOURCE_feedback_files_import > /home/pms_plus/log/crontab/ticket_transaction/ipass/ipass_feedback_files_import.log 2>&1 &"; } | crontab -
fi