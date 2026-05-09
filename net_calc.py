from flask import Flask, render_template_string, request
import ipaddress

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Network Web Tool</title>
    <style>
        body { font-family: sans-serif; background: #0f172a; color: white; text-align: center; padding: 50px; }
        .card { background: #1e293b; padding: 20px; border-radius: 15px; display: inline-block; width: 400px; }
        input { padding: 10px; border-radius: 5px; border: none; width: 80%; margin-bottom: 10px; color: black; }
        button { padding: 10px 20px; background: #2563eb; color: white; border: none; border-radius: 5px; cursor: pointer; }
        pre { text-align: left; background: #0f172a; padding: 15px; border-radius: 10px; margin-top: 20px; white-space: pre-wrap; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Network Analyzer</h2>
        <form method="POST">
            <input type="text" name="ip" placeholder="e.g. 192.168.1.1/24" required>
            <button type="submit">Analyze</button>
        </form>
        {% if result %}
        <pre>{{ result }}</pre>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        ip_input = request.form.get('ip')
        try:
            net = ipaddress.ip_network(ip_input, strict=False)
            first_octet = int(str(net.network_address).split('.')[0])
            
            if 1 <= first_octet <= 126: ip_cls = "A"
            elif 128 <= first_octet <= 191: ip_cls = "B"
            elif 192 <= first_octet <= 223: ip_cls = "C"
            else: ip_cls = "Special"

            res_data = {
                "IP Class": ip_cls,
                "Subnet Mask": str(net.netmask),
                "Network ID": str(net.network_address),
                "Broadcast ID": str(net.broadcast_address),
                "Total Hosts": net.num_addresses,
                "Usable Hosts": max(0, net.num_addresses - 2)
            }
            
            result = "\n".join([f"{k}: {v}" for k, v in res_data.items()])
            
        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template_string(HTML_TEMPLATE, result=result)
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)


