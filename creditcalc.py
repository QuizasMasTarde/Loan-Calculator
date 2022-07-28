import math
import argparse


def nominal_interest(a):
    return a / 1200


# Checks for negative values in arguments
def positive_check(a):
    for i in a:
        if i is None:
            pass
        elif i < 0:
            print('Incorrect parameters')
            exit()


#  Calculates loan principal taking annuity payment(a),
#  number of payments(n), interest rate(i) and rounds it
def loan_principal_calc(a, n, i):
    return round(a / ((nominal_interest(i) * math.pow((1 + nominal_interest(i)), n)) /
                      (math.pow((1 + nominal_interest(i)), n) - 1)))


#  Calculates monthly payment taking loan principal(p),
#  number of payments(n), interest rate(i) and rounds it to next whole value
def payment_calc(p, n, i):
    return math.ceil(p * (nominal_interest(i) * math.pow((1 + nominal_interest(i)), n)) /
                         (math.pow((1 + nominal_interest(i)), n) - 1))


#  Calculates number of payments taking loan principal(p),
#  annuity payment(a), interest rate(i) and rounds it to next whole value
def number_payments_calc(p, a, i):
    return math.ceil(math.log(a/(a - nominal_interest(i) * p), 1 + nominal_interest(i)))


#  Converts number of payments into years and months
def months_to_years(m):
    yy = m // 12
    mm = m % 12
    str_mm = 'month'
    str_yy = 'year'
    if yy != 1:
        str_yy += 's'
    if mm != 1:
        str_mm += 's'
    return yy, str_yy, mm, str_mm


#  Calculates differentiated payment taking loan principal(p),
#  number of payments(n), interest rate(i) and rounds it to the next
#  whole value. Prints payments for each month, calculates and prints overpayment
def diff_payment_calc(p, n, i):
    total = 0
    for m in range(1, n + 1):
        diff_payment = math.ceil(p / n + nominal_interest(i) * (p - p * (m - 1) / n))
        total += diff_payment
        print(f'Month {m}: payment is {diff_payment}')
    over_payment = total - p
    print(f'\nOverpayment = {over_payment}')


parser = argparse.ArgumentParser()

parser.add_argument("--type", choices=["annuity", "diff"], required=True)
parser.add_argument("--principal", type=int)
parser.add_argument("--periods", type=int)
parser.add_argument("--interest", type=float)
parser.add_argument("--payment", type=int)

args = parser.parse_args()

values = [args.principal, args.periods, args.interest, args.payment]

positive_check(values)

if values.count(None) > 1 or args.interest is None or args.type == "diff" and args.payment:
    print("Incorrect parameters")

else:
    if args.type == "diff":
        diff_payment_calc(args.principal, args.periods, args.interest)

    elif args.type == "annuity" and not args.periods:
        number_payments = number_payments_calc(args.principal, args.payment, args.interest)
        overpayment = number_payments * args.payment - args.principal
        years, str_years, months, str_months = months_to_years(number_payments)
        print('It will take', f'{years} {str_years}' if years else '', 'and' if years and months else '',
              f'{months} {str_months}' if months else '', 'to repay this loan!')
        print(f'Overpayment = {overpayment}')

    elif args.type == "annuity" and not args.payment:
        payment = payment_calc(args.principal, args.periods, args.interest)
        overpayment = args.periods * payment - args.principal
        print(f'Your annuity payment = {payment}!')
        print(f'Overpayment = {overpayment}')

    elif args.type == "annuity" and not args.principal:
        loan_principal = loan_principal_calc(args.payment, args.periods, args.interest)
        overpayment = args.periods * args.payment - loan_principal
        print(f'Your loan principal = {loan_principal}!')
        print(f'Overpayment = {overpayment}')
