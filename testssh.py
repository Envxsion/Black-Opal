from pyngrok import ngrok

# <NgrokTunnel: "tcp://0.tcp.ngrok.io:18880" -> "localhost:22">
ssh_tunnel = ngrok.connect(22, "tcp")