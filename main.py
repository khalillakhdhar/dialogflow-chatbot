import json
from flask import Flask, request, make_response, jsonify

import datetime
import calendar

app = Flask(__name__)
log = app.logger

@app.route('/', methods=['POST'])
def webhook():
    """This method handles the http requests for the Dialogflow webhook
    This is meant to be used in conjunction with the Banking Dialogflow agent
    """
    req = request.get_json(silent=True, force=True)
    try:
        action = req.get('result').get('action')
    except AttributeError:
        return 'json error'

    if action == 'check_balance':
        res = check_balance(req)

    elif action == 'get_transactions':
        res = get_transactions(req)

    elif action == 'get_cibilscore':
        res = chatbot(req)
        if cibil<650:
            res = res + '\n' + 'I see you have a low CIBIL score. Want to know how you can improve it? Check out: https://www.rediff.com/getahead/report/money-7-quick-steps-to-improve-your-cibil-score/20150921.htm'

    elif action == 'loan_eligibility':
        res = chatbot(req)

    elif action == 'account.spending.check':
        res = chatbot(req)

    return make_response(jsonify({"agent": res}))

def check_balance(req):
    parameters = req['result']['parameters']

    print('Dialogflow parameters:')
    print(json.dumps(parameters, indent=4))

    if parameters.get('account'):
        if str(parameters.get('account')) == str('savings'):
            records = MySQL("select Balance from account where AccountType='Savings';'")

            for row in records:
                bal = row[0]
                return 'Your Savings balance is: %s' % bal

        elif str(parameters.get('account')) == str('current'):
            records = MySQL("select Balance from account where AccountType='Current';")

            for row in records:
                bal = row[0]
                return 'Your Current balance is: %s' % bal


def get_transactions(req):
    parameters = req['result']['parameters']
    given_name = " " if parameters.get('given-name')=='' else "AND Description Like '%{}%'".format(parameters.get('given-name'))
    #given_name = "AND Description='{}'".format(parameters.get('given-name') if parameters.get('given-name') != '' else " ")
    date_now = datetime.datetime.now()
    type_tran = "('neft'and'imps'and'Withdraw')" if parameters.get('transaction')=='' else parameters.get('transaction')
    if parameters.get('transaction'):
        type_tran = "'%s'"%type_tran
    num_tran = '5' if parameters.get('number')=='' else parameters.get('number')
    accType_tran = "('savings'and'current')" if parameters.get('account')=='' else parameters.get('account')
    if parameters.get('account'):
        accType_tran = "'%s'"%accType_tran

    if parameters.get('date'):
        date_tran = parameters.get('date')
        year,month,day = date_tran.split('-', 3)
        year = int(year)
        month = int(month)
        day = int(day)
        start_date = datetime.datetime(year,month,1).strftime("%Y-%m-%d")
        end_date = datetime.datetime(year,month,calendar.mdays[month]).strftime("%Y-%m-%d")
        print(start_date,end_date)
    else:
        datePeriod_tran = date_now.strftime("%m-%d-%Y") if parameters.get('date-period')=='' else parameters.get('date-period')
        if datePeriod_tran != parameters.get('date-period'):
            start_date = datetime.datetime(date_now.year,1,1).strftime("%Y-%m-%d")
            end_date = datetime.datetime(date_now.year,date_now.month,calendar.mdays[date_now.month]).strftime("%Y-%m-%d")
        else:
            start_date,end_date = datePeriod_tran.split('/', 1)


   

if __name__ == '__main__':
    app.run()