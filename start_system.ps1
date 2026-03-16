Write-Host "Starting Distributed File Converter..."

Start-Process powershell -ArgumentList "cd workers; python worker.py W1 6001"
Start-Process powershell -ArgumentList "cd workers; python worker.py W2 6002"
Start-Process powershell -ArgumentList "cd workers; python worker.py W3 6003"

Start-Sleep -Seconds 2

Start-Process powershell -ArgumentList "cd gateway; javac Gateway.java; java Gateway"

Start-Sleep -Seconds 2

Start-Process powershell -ArgumentList "cd client; python client.py"