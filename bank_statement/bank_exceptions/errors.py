class BankAccountTypeError(Exception):
    '''
    exception raised when the user uploads more than 1 bank statement for an individual
    '''
    def __init__(self, bank_account_type, message="There are too many uploaded documents"):
        self.bank_account_type_list = bank_account_type
        self.message = message
        super().__init__(self.message)
        
    def __str__(self):
        return "You must upload one statement per individual (SAVINGS/CURRENT) bank statement per individual"

class BankStatementPathError(Exception):
    '''
    exception raised when the path is incorect
    '''
    def __init__(self, message="The Bank statement path does not exist"):
        self.message = message
        super().__init__(self.message)
        
    def __str__(self):
        return "Check that there is no typo in the bank statement filepath"

class BankStatementFormatError(Exception):
    '''
    exception raised when the extension of the file is incorrect (.pdf only)
    '''
    def __init__(self, message="The Bank statement format is not accepted"):
        self.message = message
        super().__init__(self.message)
        
    def __str__(self):
        return "The valid format is pdf - only"

class BankStatementColumnsError(Exception):
    '''
    depending on the table the columns must have a predefined number of columns (defined by the mapping)
    '''
    def __init__(self, template_version, bank_id, mapping):

        
        message = f"DataFrames format should have at max: {mapping[bank_id][template_version]}"
        self.message = message
        super().__init__(self.message)
        
    def __str__(self):
        return "There is a problem of columns during extraction"
