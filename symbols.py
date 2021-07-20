"""Update the json list if more words need to get recognised"""
symbol = {
    'alpha': 'α',
    'beta': 'β',
    'gamma': 'γ',
    'lambda': 'λ',
    'plus': '+',
    'add': '+',
    'subtract': '-',
    'minus': '-',
    'into': '*',
    'multiply': 'X',
    'divide': '/',
    'by': '/',
    'percentage': '%',
    'mod': '%',
    'theta': 'θ',
    'integration': '∫',
    'derivative': '∂',
    'differentiation': '∂',
    'equal to': '=',
    'equals to': '=',
    'equas': '='
}


def get():
    # export the symbol list
    return symbol
