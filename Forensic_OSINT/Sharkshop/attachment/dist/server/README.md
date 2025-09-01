
Run the following for testing locally
```
openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout nginx/key.pem -out nginx/cert.pem -subj "/CN=localhost"  
```