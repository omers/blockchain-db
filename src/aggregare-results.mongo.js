db.blocks.aggregate(
   [
    { $unwind: {"path": "$transactions"}},
    { $unwind: {"path": "$transactions.transaction_info.sender"}},
    { $match: { "transactions.transaction_info.recipient": {$ne: "00000000000000000000x1" }} },
    // { $unwind: {"path": "$transactions.transaction_info.transaction_id"}},
     {
        $group:
         {
           _id: "$transactions.transaction_info.recipient",
           votes: {$sum: 1}
         }
     }
   ]
)
