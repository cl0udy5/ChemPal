import chemparse
from fractions import Fraction
import math
import copy

output = {
    'correct_input': True,
    'initial_check': True,
    'is_combustion': False,
    'equation': '',
    'elements_reactants': [],
    'elements_products': [],
    'initial_equations': {},
    'adjusted_equations': {},
    'coefficient_matrix': [],
    'solved_matrix': [],
    'unbalanced_coefficients': '',
    'balanced_coefficients': '',
    'answer': ''
}

def Combustion_percentage(answer, products):
    global output
    answer_sep = answer.replace(' ', '')
    m = list(answer_sep.split('='))
    reactants_balanced = m[0].split('+')
    products_balanced = m[1].split('+')
    elements_reactants = [custom_parse(i) for i in reactants_balanced]
    elements_products = [custom_parse(i) for i in products_balanced]
    for dict_reactant in elements_reactants:
        if 'O' in dict_reactant:
            O_reactant = dict_reactant['O']/2
    if 'CO2' in products and 'H2O' in products:
        print('This combustion is 100% complete')
        output['is_combustion'] = True
        output['combustion'] = 'This combustion is 100% complete'
    elif 'H2O' in products and 'CO' in products:
        for dict_product in elements_products:
           if 'H' not in dict_product:
                O_product = dict_product['O']
        percentage =  O_reactant * 100/(O_reactant + (O_product/2))
        print("This combustion is {:.2f} % complete".format(percentage))
        output['is_combustion'] = True
        output['combustion'] = "This combustion is {:.2f} % complete".format(percentage)
    elif 'H2O' in products and 'C' in products:
        for dict_product in elements_products:
           if 'H' not in dict_product:
                O_product = dict_product['C'] 
        percentage =  O_reactant * 100/(O_reactant + O_product)
        print("This combustion is {:.2f} % complete".format(percentage))
        output['is_combustion'] = True
        output['combustion'] = "This combustion is {:.2f} % complete".format(percentage)

def custom_parse(mol: str) -> dict:
    elements = {}
    name = ''
    amount = ''
    multiplier = ''
    for i in range(len(mol)):
        if mol[i].isdigit():
            multiplier += mol[i]
        else:
            start = i
            break
    if multiplier == '':
        multiplier = '1'
    multiplier = int(multiplier)
    for i in range(start, len(mol)):
        if mol[i].isupper():
            if name != '':
                if amount == '':
                    amount = '1'
                if name in elements:
                    elements[name] += int(amount) * multiplier
                else:
                    elements[name] = int(amount) * multiplier
            name = mol[i]
            amount = ''
        elif mol[i].islower():
            name += mol[i]
        elif mol[i].isdigit():
            amount += mol[i]
        elif mol[i] == '(':
            if amount == '':
                amount = '1'
            if name in elements:
                elements[name] += int(amount) * multiplier
            else:
                elements[name] = int(amount) * multiplier
            multiplier *= int(mol[mol.find(')') + 1: ])
            name = ''
            amount = ''
        elif mol[i] == ')':
            if amount == '':
                amount = '1'
            if name in elements:
                elements[name] += int(amount) * multiplier
            else:
                elements[name] = int(amount) * multiplier
            name = ''
            break
    if name != '':
        if amount == '':
            amount = '1'
        if name in elements:
            elements[name] += int(amount) * multiplier
        else:
            elements[name] = int(amount) * multiplier
    return elements

def multiply_row(final_matrix: list, a,b,row,column : int) -> list:
    for i in range(len(final_matrix[column])):
        final_matrix[column][i] *= b
    for i in range(len(final_matrix[row])):
        final_matrix[row][i] *= a
    return final_matrix


def subtract_row(final_matrix: list, row, column, b: int) -> list:
    for i in range(len(final_matrix[row])):
        final_matrix[row][i] -= final_matrix[column][i]
        final_matrix[column][i] //= b
    return final_matrix

def solve(final_matrix: list) -> list:
    for row in range(1, len(final_matrix)):
        for column in range(row):
            if final_matrix[row][column] != 0:
                a = final_matrix[column][column]
                b = final_matrix[row][column]
                final_matrix = multiply_row(final_matrix, a, b, row, column)
                final_matrix = subtract_row(final_matrix, row, column, b)
    for row in range(len(final_matrix)):
        denominator = final_matrix[row][row]
        for column in range(len(final_matrix) + 1):
            if denominator != 0:
                final_matrix[row][column] /= denominator
    return final_matrix

def get_eq(elements_reactants, elements_products: dict, reactants: list, products: list, variables:list) -> dict:
    equations = {}
    checking_prodcuts = []
    for i in range(len(reactants)):
        for key in elements_reactants[i]:
            if key in equations:
                equations[key] += '+' + str(int(elements_reactants[i][key])) + f'*{variables[i]}'
            else:
                equations[key] = str(int(elements_reactants[i][key])) + f'*{variables[i]}'
    j = i + 1
    for i in range(len(products)):
        for key in elements_products[i]:
            if key in checking_prodcuts:
                equations[key] += '+' + str(int(elements_products[i][key])) + f'*{variables[i + j]}'
            else:
                equations[key] += '=' + str(int(elements_products[i][key])) + f'*{variables[i + j]}'
                checking_prodcuts.append(key)
    return equations

def list_of_rows_in_order(lines: dict, s: str, key, index_of_value: int) -> str:
    row = str(lines[key][index_of_value])
    if len(s) == len(lines):
        return s
    if key == len(lines) - 1 and index_of_value == len(lines[key]) - 1 and len(s) < len(lines):
        if row not in s:
            return list_of_rows_in_order(lines, s + row, key, index_of_value)
        return ''
    if key < len(lines) - 1:
        if index_of_value < len(lines[key]) - 1:
            if row not in s:
                return list_of_rows_in_order(lines, s + row, key + 1, 0) + list_of_rows_in_order(lines, s, key, index_of_value + 1)
            else:
                return list_of_rows_in_order(lines, s, key, index_of_value + 1)
        else:    
            if row not in s:
                return list_of_rows_in_order(lines, s + row, key + 1, 0) + list_of_rows_in_order(lines, s, key + 1, 0)
            else:
                if len(s) < key:
                    return ''
                else:
                    return list_of_rows_in_order(lines, s, key + 1, 0)
    else:
        if row not in s:
            return list_of_rows_in_order(lines, s + row, key, index_of_value + 1)
        else:
            return list_of_rows_in_order(lines, s, key, index_of_value + 1)

def adjust_matrix(x: list) -> list:
    apr_lines = {}
    for i in range(len(x[0]) - 1):
        for j in range(len(x)):
            if x[j][i] != 0:
                if i in apr_lines:
                    apr_lines[i].append(j)
                else:
                    apr_lines[i] = list()
                    apr_lines[i].append(j)
    s = list_of_rows_in_order(apr_lines, '', 0, 0)[:len(x[0]) - 1]
    adjusted_matrix = [x[int(i)] for i in s]
    return adjusted_matrix

def adjust_eq_new(x: dict, variables: list) -> dict:
    equations_in_func = x
    for i in equations_in_func:
            index_of_eq = equations_in_func[i].index('=')
            right_equation = equations_in_func[i][index_of_eq + 1:]
            equations_in_func[i] = equations_in_func[i][:index_of_eq]
            j = 0
            while right_equation != '':
                if right_equation[j].isalpha():
                    if right_equation[j] == variables[-1]:
                        equations_in_func[i] += '=' + right_equation
                        right_equation = ''
                    else:
                        equations_in_func[i] += '-' + right_equation[:j + 1]
                        if j + 1 == len(right_equation):
                            right_equation = ''
                            equations_in_func[i] += f'=0*{variables[-1]}'
                        else:
                            right_equation = right_equation[j + 2:]
                        j = 0
                else:
                    j += 1
    return equations_in_func

def lcm(a, b: int) -> int:
    return (a * b) // math.gcd(a, b)

def create_matrix_new(variables: list, equations: dict) -> list:
    x = []
    sub_x = []
    j = 0
    for i in equations:
        s = equations[i]
        while s != '':
            if s[s.index('*') + 1] == variables[j]:
                sub_x.append(int(s[:s.index('*')]))
                s = s[s.index('*') + 2:]
                if s == '':
                    break
                elif s[0] == '+':
                    s = s[s.index('+') + 1:]
                elif s[0] == '-':
                    s = s[s.index('-'):]
                elif s[0] == '=':
                    s = s[s.index('=') + 1:]
                else:
                    s = ''
            else:
                sub_x.append(0)
            j += 1
        x.append(sub_x)
        sub_x = []
        j = 0
    return x

def convert_matrix_to_fractions(matrix):
    fraction_matrix = []
    for row in matrix:
        fraction_row = [Fraction(item).limit_denominator() for item in row]
        fraction_matrix.append(fraction_row)
    return fraction_matrix


def extract_final_equations(variables: list, solved_matrix: list) -> list:
    global output
    ans = []
    ans.append(1)
    for i in range(len(solved_matrix) - 1, -1, -1):
        v = solved_matrix[i][-1]
        for j in range(len(solved_matrix[0]) - 2, i, -1):
            v += solved_matrix[i][j] * -1 * ans[j - 1]
        ans.append(v)
    ans.reverse()
    ans_ratio = []
    multiplier = 1
    for value in ans:
        ans_ratio.append(str(Fraction(value).limit_denominator()))
    output['unbalanced_coefficients'] = ', '.join(f'{variables[i].upper()}: {ans_ratio[i]}' for i in range(len(ans_ratio)))
    for i in range(len(ans_ratio)):
        if '/' in ans_ratio[i]:
            x = int(ans_ratio[i][ans_ratio[i].index('/') + 1:])
            multiplier = lcm(multiplier, x)
    for i in range(len(ans)):
        ans[i] *= multiplier
    return ans


def final_solution(s: str) -> list:
    output['equation'] = s
    answer = s
    s = s.replace(' ', '')
    s = s.replace('->', '=')
    m = list(s.split('='))
    reactants = m[0].split('+')
    products = m[1].split('+')
    # elements_reactants = []
    # elements_products = []
    # for i in reactants:
    #     elements_reactants.append(chemparse.parse_formula(i))
    # for i in products:
    #     elements_products.append(chemparse.parse_formula(i))
    elements_reactants = [custom_parse(i) for i in reactants]
    elements_products = [custom_parse(i) for i in products]
    output['elements_reactants'] = elements_reactants
    output['elements_products'] = elements_reactants
    output['initial_check'] = True
    total_elements_reactants= {}
    total_elements_products = {}

    for i in elements_reactants:
        for j in i:
            if j in total_elements_reactants:
                total_elements_reactants[j] += i[j]
            else:
                total_elements_reactants[j] = i[j]

    for i in elements_products:
        for j in i:
            if j in total_elements_products:
                total_elements_products[j] += i[j]
            else:
                total_elements_products[j] = i[j]

    for i in total_elements_products:
        if total_elements_products[i] != total_elements_reactants[i]:
            output['initial_check'] = False

    if not output['initial_check']:   
        variables = [chr(i) for i in range(97, 97 + len(reactants) + len(products))]
        equations = get_eq(elements_reactants, elements_products, reactants, products, variables)
        a = equations
        output['variables'] = variables

        output['initial_equations'] = a

        adjusted_equations = adjust_eq_new(copy.deepcopy(equations), variables)

        output['adjusted_equations'] = adjusted_equations
        final_matrix = create_matrix_new(variables, adjusted_equations)

        output['coefficient_matrix'] = convert_matrix_to_fractions(final_matrix)

        final_matrix = adjust_matrix(final_matrix)

        output['coefficient_adjusted_matrix'] = convert_matrix_to_fractions(final_matrix)

        solved_matrix = solve(final_matrix)

        output['solved_matrix'] = convert_matrix_to_fractions(solved_matrix)
        
        list_of_coefficients = extract_final_equations(variables, solved_matrix)
        
        output['balanced_coefficients'] = ', '.join(f'{variables[i].upper()}: {int(list_of_coefficients[i])}' for i in range(len(list_of_coefficients)))
        molecules = reactants
        j = 0
        answer = ''
        for i in list_of_coefficients:
            if i != 1:
                if molecules[j][0].isalpha():
                    answer += str(int(i)) + molecules[j] + ' '
                else:
                    sub_molecule = ''
                    for numbers in molecules[j]:
                        if numbers.isdigit():
                            sub_molecule += numbers
                        else:
                            first_letter = numbers
                            break
                    answer += str(int(i) * int(sub_molecule)) + molecules[j][molecules[j].find(first_letter):] + ' '
            else:
                answer += molecules[j] + ' '
            j += 1
            if j == len(molecules):
                if molecules == reactants:
                    molecules = products
                    answer += '= '
                j = 0
            else:
                answer += '+ '
        output['answer'] = answer
    Combustion_percentage(answer, products)
    return(output)


if __name__ == '__main__':
    print(final_solution('PhCH3 + KMnO4 + H2SO4 = PhCOOH + K2SO4 + MnSO4 + H2O'))



# H2 + O2 = H2O
# CH4 + O2 = CO2 + H2O
# CO2 + H2O = O2 + C6H12O2
# Fe2(SO4)3 + KOH = K2SO4 + Fe(OH)3
# Mg + O2 = MgO
# Fe + HCl = FeCl2 + H2
# BrO3 + 2H + Br = HBrO2 + HOBr
# K + MgBr = KBr + Mg
# FeCl3 + NaOH = Fe(OH)3 + NaCl
# C8H18 + O2 = CO2 + H2O
# C3H8 + O2 = CO2 + H2O
# CH4 + O2 = CO2 + H2O