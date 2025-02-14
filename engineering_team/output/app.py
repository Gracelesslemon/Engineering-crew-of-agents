import gradio as gr
from accounts import Account

account = Account("user123")

def deposit(amount):
    if account.deposit(float(amount)):
        return f"Deposit successful. New balance: {account.get_balance()}"
    else:
        return "Deposit failed. Please enter a positive amount."

def withdraw(amount):
    if account.withdraw(float(amount)):
        return f"Withdrawal successful. New balance: {account.get_balance()}"
    else:
        return "Withdrawal failed. Insufficient funds."

def buy(symbol, quantity):
    if account.buy_shares(symbol, int(quantity)):
        return f"Buy successful. New balance: {account.get_balance()}. Holdings: {account.get_holdings()}"
    else:
        return "Buy failed. Insufficient funds or invalid quantity."

def sell(symbol, quantity):
    if account.sell_shares(symbol, int(quantity)):
        return f"Sell successful. New balance: {account.get_balance()}. Holdings: {account.get_holdings()}"
    else:
        return "Sell failed. Insufficient shares."

def get_portfolio():
    return f"Portfolio Value: {account.get_portfolio_value():.2f}"

def get_profit():
    return f"Profit/Loss: {account.get_profit_loss():.2f}"

def get_transactions():
    transactions = account.get_transactions()
    if not transactions:
        return "No transactions yet."
    
    output = "Transactions:\n"
    for transaction in transactions:
        output += f"{transaction['timestamp']}: {transaction['type']}"
        if 'symbol' in transaction:
            output += f" {transaction['symbol']}"
        if 'quantity' in transaction:
            output += f" x{transaction['quantity']}"
        if 'price' in transaction:
            output += f" @{transaction['price']}"
        if 'amount' in transaction:
            output += f" ${transaction['amount']}"
        output += "\n"
    return output

with gr.Blocks() as demo:
    gr.Markdown("# Trading Account Simulator")

    with gr.Tab("Account Actions"):
        with gr.Row():
            deposit_amount = gr.Textbox(label="Deposit Amount")
            deposit_button = gr.Button("Deposit")
            deposit_output = gr.Textbox(label="Deposit Status")
        deposit_button.click(fn=deposit, inputs=deposit_amount, outputs=deposit_output)

        with gr.Row():
            withdraw_amount = gr.Textbox(label="Withdraw Amount")
            withdraw_button = gr.Button("Withdraw")
            withdraw_output = gr.Textbox(label="Withdraw Status")
        withdraw_button.click(fn=withdraw, inputs=withdraw_amount, outputs=withdraw_output)

    with gr.Tab("Trade"):
        with gr.Row():
            symbol = gr.Textbox(label="Symbol (AAPL, TSLA, GOOGL)")
            quantity = gr.Textbox(label="Quantity")
            buy_button = gr.Button("Buy")
            buy_output = gr.Textbox(label="Buy Status")
        buy_button.click(fn=buy, inputs=[symbol, quantity], outputs=buy_output)

        with gr.Row():
            symbol_sell = gr.Textbox(label="Symbol (AAPL, TSLA, GOOGL)")
            quantity_sell = gr.Textbox(label="Quantity")
            sell_button = gr.Button("Sell")
            sell_output = gr.Textbox(label="Sell Status")
        sell_button.click(fn=sell, inputs=[symbol_sell, quantity_sell], outputs=sell_output)

    with gr.Tab("Reports"):
        portfolio_button = gr.Button("Get Portfolio Value")
        portfolio_output = gr.Textbox(label="Portfolio Value")
        portfolio_button.click(fn=get_portfolio, outputs=portfolio_output)

        profit_loss_button = gr.Button("Get Profit/Loss")
        profit_loss_output = gr.Textbox(label="Profit/Loss")
        profit_loss_button.click(fn=get_profit, outputs=profit_loss_output)

        transactions_button = gr.Button("Get Transactions")
        transactions_output = gr.Textbox(label="Transactions")
        transactions_button.click(fn=get_transactions, outputs=transactions_output)

demo.launch()
