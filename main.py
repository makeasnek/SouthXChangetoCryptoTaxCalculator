import csv
from typing import Dict,List
import datetime

# function to update dictionary of trades
def update_trade_dict(fields:Dict[str,str])->bool:
    """

    :param fields: transaction to import/merge, must have trade_id field
    :return: True if a matching transaction found + merged, false if new transaction created
    """
    for transaction in final_transactions:
        if 'trade_id' not in transaction:
            continue
        if transaction['trade_id']==fields['trade_id']:
            #print('For transaction A found matching B: \nA: {}\nB: {}'.format(fields,transaction))
            for key,value in fields.items():
                transaction[key]=value
            return True
    #print('Making new transaction: {}'.format(fields))
    final_transactions.append(fields)
    return False

# read in CSV file
with open('import.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    # convert fields to appropriate ones for cryptotaxcalculator.io
    final_transactions:List[Dict[str,str]] = []
    for entry in reader:
        transaction_type = entry['Type'].upper()

        #Convert time into format used by CryptoTaxCalculator
        datetime_object = datetime.datetime.strptime(entry['Date_UTC'], '%Y-%m-%dT%H:%M:%S.%f')
        final_date=datetime_object.strftime('%Y-%m-%d %H:%M:%S')

        #Declare universal fields
        temp_dict:Dict[str,str] = {
            'Timestamp (UTC)': final_date,
            'ID (optional)': entry['Id'],
        }
        if transaction_type == 'DEPOSIT':
            temp_dict['Type'] = 'transfer-in'
            temp_dict['Base Currency'] = entry['Currency']
            temp_dict['Base Amount'] = entry['Delta']
            #temp_dict['To (Optional)'] = entry['Deposit_Address'] # disabled this, when enabled, cryptotaxcalculator doesn't seem to recognize this transaction correctly.
            final_transactions.append(temp_dict)
            continue
        elif transaction_type == 'WITHDRAWAL':
            temp_dict['Type']='transfer-out'
            temp_dict['Base Currency'] = entry['Currency']
            amount=abs(float(entry['Delta']))
            amount_string=f"{amount:.12f}"
            temp_dict['Base Amount'] = amount_string
            temp_dict['To (Optional)']=entry['Withdraw_Address']
            final_transactions.append(temp_dict)
            continue
        elif transaction_type=='TRADE':
            temp_dict['Type']='sell'
            temp_dict['trade_id'] = entry['Trade_Id']
            delta=float(entry['Delta'])
            delta_abs=abs(delta)
            delta_string=f"{delta_abs:.12f}"
            if delta<0: # the currency you sold
                temp_dict['Base Currency'] = entry['Currency']
                temp_dict['Base Amount'] = delta_string
            elif delta>0: # the currency you bought/exchanged it for
                temp_dict['Quote Currency'] = entry['Currency']
                temp_dict['Quote Amount'] = delta_string
            update_trade_dict(fields=temp_dict)
            continue
        elif transaction_type == 'FEE':
            temp_dict['Fee Currency (Optional)'] = entry['Currency']
            amount = abs(float(entry['Delta']))
            amount_string = f"{amount:.12f}"
            temp_dict['Fee Amount (Optional)'] = amount_string
            trade_id=entry['Trade_Id']
            # if this is from a trade, mark it as such
            if trade_id!='':
                temp_dict['Type']='sell'
                temp_dict['trade_id'] = entry['Trade_Id']
                update_trade_dict(fields=temp_dict)
                continue
            # otherwise just count it as a general fee
            else:
                temp_dict['Type'] = 'fee'
                final_transactions.append(temp_dict)
                continue
        else:
            print('Warning: Found unknown transaction type: {}, skipping...'.format(transaction_type))

# write out final CSV
with open('output.csv','w') as a_file:
    # Setup header in order that cryptotaxcalculator wants
    key_list = ['Timestamp (UTC)', 'Type', 'Base Currency', 'Base Amount', 'Quote Currency', 'Quote Amount',
                'Fee Currency (Optional)', 'Fee Amount (Optional)', 'From (Optional)', 'To (Optional)', 'ID (optional)',
                'Description (Optional)']
    dict_writer = csv.DictWriter(a_file, key_list)
    dict_writer.writeheader()
    for transaction in final_transactions:
        if 'trade_id' in transaction:
            del transaction['trade_id']
        dict_writer.writerow(transaction)
