from flask import Flask, request
from binance.um_futures import UMFutures
import threading

app = Flask(__name__)

API_KEY = "mRAh2D1DKn2NgSO1p9Z3606dneX qKVTDICWZSpQg2Ty7hboCATG8nsi 4HpHBoinf"
API_SECRET = "cWMAVqTMHiqgE0VQiiDkhrukqccuh OG4GV3UguvWwzulhkiXFbORZzJpD TM5NN8i"
client = UMFutures(key=API_KEY, secret=API_SECRET)

symbol = "SOLUSDT"
quantity = 1  # update as per your trade size

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("Received data:", data)

    if data and data.get("action") == "sell":
        entry_price = float(data["entry"])
        tp_ratio = float(data["tp_ratio"])
        sl_ratio = float(data["sl_ratio"])

        tp = round(entry_price - (entry_price * tp_ratio / 100), 2)
        sl = round(entry_price + (entry_price * sl_ratio / 100), 2)

        # Place SELL order
        response = client.new_order(
            symbol=symbol,
            side="SELL",
            type="MARKET",
            quantity=quantity
        )

        print("Sell Order Response:", response)
        print(f"Placed short entry at {entry_price}, TP: {tp}, SL: {sl}")
        return {"status": "Sell order placed"}
    
    return {"error": "Invalid data or not a sell signal"}

def run_app():
    app.run(host='0.0.0.0', port=8080)

# Start Flask in background thread
threading.Thread(target=run_app).start()