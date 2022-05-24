import os
import logging

def log_info(step, account_type, bank_id, statement_gt_bank, error, **kwargs):
    '''
    create a custom logger to store each step and info/error when needed
    TBD : **kwargs 
    '''
    extension = os.path.splitext(f'{statement_gt_bank}')[1][:]
    rel_logname = f'{statement_gt_bank}'.replace(extension,".log").split("/")[-1]
    logname = os.path.join(os.getcwd(), rel_logname)
    
    FORMAT = '%(asctime)-15s %(bank_account_type)s %(bank_file_name)-15s %(error_message)s %(message)s'

    # using the keyword force=True is necessary to avoid blank pages when logging
    logging.basicConfig(filename=logname,
                        filemode='a',
                        format=FORMAT,
                        force=True,
                        level=logging.INFO)

    d = {
        'bank_account_type': account_type,
        'step':step,
        'bank_id': bank_id, 
        'bank_file_name': statement_gt_bank,
        'error_message': str(error)
        }

    
    logger = logging.getLogger('bank_statement')
    if error != None:
        logger.info('ETL_STEP_%s', step, extra=d)
    else:
        logger.error('ETL_STEP_%s', step, extra=d)