# SouthXChangetoCryptoTaxCalculator
This python script will help you convert your exported transactions from SouthXChange into a format that cryptotaxcalculator.io likes. It currently handles deposits, withdrawals, and trades, but not buys or sells (if you are using fiat currency). It is written for Python3 and above.

<b>Before using this software, if you haven't gotten too deep into using CryptoTaxCalculator yet, I would implore you to use another website. I would unequivocally review their service's functionality as "hot garbage" dusted with a light sprinkle of "dumpster juice".</b> I have verified that this script outputs data in the correct format, but that will unfortunately will not help much because:
* CryptoTaxCalculator seems to struggle reconciling time zones even when amounts, source, and destination are specified
* Even with two public addresses using their own import method, it can't correctly detect transfers between them. This bug exists in Bitcoin, not some random altcoin that nobody has heard about which you are using SouthExchange to trade
* I went back and forth for WEEKS with their support staff and was eventually told that they know their import system from "non-specific top 5 by volume crypto exchange" is broken but that there's nothing they can do about it and we're oh so sorry that you couldn't file your taxes on time because of it. Actually, they didn't apologize for the delay in not solving the issue or that their software doesn't even provide the basic functionality promised.

How to use:
1. Save your SouthXChange trades export as "import.csv" and put it in the same directory as the script.
2. Run the script
3. See output.csv which you can import into cryptotaxcalculator.io

This software is produced AS IS without ANY WARRANTY. It works well for me, it may not work perfectly for you. Be sure to double-check any numbers it comes up with. This software is released into the public domain. It will never be updated, because I see no reason why any sane person would use CryptoTaxCalculator, and since I like to imagine myself among the sane I will not use it in the future.

