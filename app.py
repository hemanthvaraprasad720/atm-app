from flask import Flask, render_template, request

app = Flask(__name__)

# In-memory accounts dictionary
accounts = {}

@app.route('/')
def home():
    return render_template('home.html', accounts=accounts)

@app.route('/home')
def home2():
    return render_template('home.html', accounts=accounts)

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'GET':
        return render_template('create.html')

    account_no = request.form.get('acc_no')
    name = request.form.get('name')
    balance = request.form.get('balance')

    if account_no in accounts:
        return render_template('create.html', message='This account already exists', msg_type='error')

    if len(account_no) != 10:
        return render_template('create.html', message='Invalid account number', msg_type='error')

    if int(balance) < 2000:
        return render_template('create.html', message='Minimum balance required is 2000', msg_type='error')

    accounts[account_no] = {'name': name, 'balance': int(balance)}
    message = 'Account created successfully !!'
    return render_template('create.html', message=message, msg_type='success')


@app.route('/balance', methods=['GET', 'POST'])
def balance():
    if request.method == 'POST':
        account_no = request.form.get('acc_no')
        if account_no in accounts:
            account = accounts[account_no]
            return render_template('balance.html', account=account, acc_no=account_no)
        else:
            return render_template('balance.html', message="Account does not exist", msg_type='error')
    return render_template('balance.html')


@app.route('/update', methods=['GET', 'POST'])
def update():
    message, balance = "", None
    if request.method == 'POST':
        account_no = request.form.get('acc_no')
        amount = int(request.form.get('amount'))
        action = request.form.get('action')

        if account_no not in accounts:
            return render_template('update.html', message="Account does not exist", msg_type='error')

        if action == 'deposit':
            accounts[account_no]['balance'] += amount
            message = f"Deposit of {amount} successful! ✅"
        elif action == 'withdraw':
            if accounts[account_no]['balance'] >= amount:
                accounts[account_no]['balance'] -= amount
                message = f"Withdrawal of {amount} successful! ✅"
            else:
                return render_template('update.html', message="Insufficient balance", msg_type='error')

        balance = accounts[account_no]['balance']
        return render_template(
            'update.html',
            message=message,
            msg_type='success',
            acc_no=account_no,
            balance=balance
        )

    return render_template('update.html')
@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        account_no = request.form.get('acc_no')

        if account_no not in accounts:
            return render_template('delete.html', 
                                   message="Account does not exist", 
                                   msg_type="error")

        del accounts[account_no]

        return render_template('delete.html', 
                               message=f"Account {account_no} deleted successfully!", 
                               msg_type="success")

    return render_template('delete.html')


if __name__ == '__main__':
    app.run(debug=True, port=5001)