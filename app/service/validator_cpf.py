import re

def validate_cpf(cpf: str) -> bool:
    """
    Validates a Brazilian CPF (Cadastro de Pessoas Físicas) number.

    Args:
        cpf: The CPF string to validate. Can contain dots and hyphens.

    Returns:
        True if the CPF is valid, False otherwise.
    """

    
    # Remove non-digit characters
    cpf = re.sub(r'\D', '', cpf)

    # CPF must have 11 digits
    if len(cpf) != 11:
        return False

    # Check for known invalid CPFs (all digits are the same)
    if cpf == cpf[0] * 11:
        return False

    # Validate first digit
    sum_digits = 0
    for i in range(9):
        sum_digits += int(cpf[i]) * (10 - i)
    
    first_verifier_digit = 11 - (sum_digits % 11)
    if first_verifier_digit > 9:
        first_verifier_digit = 0
    
    if int(cpf[9]) != first_verifier_digit:
        return False

    # Validate second digit
    sum_digits = 0
    for i in range(10):
        sum_digits += int(cpf[i]) * (11 - i)
    
    second_verifier_digit = 11 - (sum_digits % 11)
    if second_verifier_digit > 9:
        second_verifier_digit = 0
    
    if int(cpf[10]) != second_verifier_digit:
        return False

    return True
