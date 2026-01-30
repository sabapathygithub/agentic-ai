import gradio as gr
from accounts import Account, get_share_price

# Initialize a single user account
account = Account("demo_user")

def deposit_funds(amount):
    try:
        account.deposit(float(amount))
        return f"Successfully deposited ${amount}. New balance: ${account.balance:.2f}"
    except Exception as e:
        return f"Error: {str(e)}"

def withdraw_funds(amount):
    try:
        account.withdraw(float(amount))
        return f"Successfully withdrew ${amount}. New balance: ${account.balance:.2f}"
    except Exception as e:
        return f"Error: {str(e)}"

def buy_shares_action(symbol, quantity):
    try:
        account.buy_shares(symbol, int(quantity))
        price = get_share_price(symbol)
        return f"Successfully bought {quantity} shares of {symbol} at ${price:.2f} each. New balance: ${account.balance:.2f}"
    except Exception as e:
        return f"Error: {str(e)}"

def sell_shares_action(symbol, quantity):
    try:
        account.sell_shares(symbol, int(quantity))
        price = get_share_price(symbol)
        return f"Successfully sold {quantity} shares of {symbol} at ${price:.2f} each. New balance: ${account.balance:.2f}"
    except Exception as e:
        return f"Error: {str(e)}"

def view_portfolio():
    portfolio_value = account.calculate_portfolio_value()
    profit_loss = account.calculate_profit_loss()
    holdings = account.get_holdings()
    
    output = f"Account: {account.username}\n"
    output += f"Cash Balance: ${account.balance:.2f}\n"
    output += f"Total Portfolio Value: ${portfolio_value:.2f}\n"
    output += f"Profit/Loss: ${profit_loss:.2f}\n\n"
    output += "Holdings:\n"
    
    if holdings:
        for symbol, quantity in holdings.items():
            price = get_share_price(symbol)
            value = price * quantity
            output += f"  {symbol}: {quantity} shares @ ${price:.2f} = ${value:.2f}\n"
    else:
        output += "  No holdings\n"
    
    return output

def view_transactions():
    transactions = account.get_transactions()
    
    if not transactions:
        return "No transactions yet"
    
    output = "Transaction History:\n\n"
    for i, txn in enumerate(transactions, 1):
        output += f"{i}. Type: {txn['type']}\n"
        
        if txn['type'] in ['deposit', 'withdrawal']:
            output += f"   Amount: ${txn['amount']:.2f}\n"
        elif txn['type'] in ['buy', 'sell']:
            output += f"   Symbol: {txn['symbol']}\n"
            output += f"   Quantity: {txn['quantity']}\n"
            output += f"   Price: ${txn['price']:.2f}\n"
            output += f"   Total: ${txn['total']:.2f}\n"
        
        output += f"   Balance after: ${txn['balance']:.2f}\n\n"
    
    return output

def get_current_prices():
    output = "Current Share Prices:\n\n"
    for symbol in ['AAPL', 'TSLA', 'GOOGL']:
        price = get_share_price(symbol)
        output += f"{symbol}: ${price:.2f}\n"
    return output

# Create Gradio interface
with gr.Blocks(title="Trading Account Demo") as demo:
    gr.Markdown("# Trading Account Management System")
    gr.Markdown("Simple demo for single user account management")
    
    with gr.Tab("Deposit/Withdraw"):
        with gr.Row():
            with gr.Column():
                gr.Markdown("### Deposit Funds")
                deposit_amount = gr.Number(label="Amount to Deposit", value=1000)
                deposit_btn = gr.Button("Deposit")
                deposit_output = gr.Textbox(label="Result")
                deposit_btn.click(deposit_funds, inputs=[deposit_amount], outputs=[deposit_output])
            
            with gr.Column():
                gr.Markdown("### Withdraw Funds")
                withdraw_amount = gr.Number(label="Amount to Withdraw", value=100)
                withdraw_btn = gr.Button("Withdraw")
                withdraw_output = gr.Textbox(label="Result")
                withdraw_btn.click(withdraw_funds, inputs=[withdraw_amount], outputs=[withdraw_output])
    
    with gr.Tab("Trade Shares"):
        gr.Markdown("### Share Prices")
        prices_display = gr.Textbox(label="Current Prices", value=get_current_prices(), lines=4)
        refresh_prices_btn = gr.Button("Refresh Prices")
        refresh_prices_btn.click(get_current_prices, outputs=[prices_display])
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("### Buy Shares")
                buy_symbol = gr.Dropdown(choices=['AAPL', 'TSLA', 'GOOGL'], label="Symbol", value='AAPL')
                buy_quantity = gr.Number(label="Quantity", value=10)
                buy_btn = gr.Button("Buy")
                buy_output = gr.Textbox(label="Result")
                buy_btn.click(buy_shares_action, inputs=[buy_symbol, buy_quantity], outputs=[buy_output])
            
            with gr.Column():
                gr.Markdown("### Sell Shares")
                sell_symbol = gr.Dropdown(choices=['AAPL', 'TSLA', 'GOOGL'], label="Symbol", value='AAPL')
                sell_quantity = gr.Number(label="Quantity", value=5)
                sell_btn = gr.Button("Sell")
                sell_output = gr.Textbox(label="Result")
                sell_btn.click(sell_shares_action, inputs=[sell_symbol, sell_quantity], outputs=[sell_output])
    
    with gr.Tab("Portfolio"):
        gr.Markdown("### View Portfolio")
        portfolio_btn = gr.Button("Refresh Portfolio")
        portfolio_output = gr.Textbox(label="Portfolio Status", lines=12)
        portfolio_btn.click(view_portfolio, outputs=[portfolio_output])
    
    with gr.Tab("Transactions"):
        gr.Markdown("### Transaction History")
        transactions_btn = gr.Button("Refresh Transactions")
        transactions_output = gr.Textbox(label="Transactions", lines=15)
        transactions_btn.click(view_transactions, outputs=[transactions_output])

if __name__ == "__main__":
    demo.launch()