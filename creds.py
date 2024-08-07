import os

mail = os.getenv('EMAIL')
password = os.getenv('PASSWORD')

if not mail or not password:
    raise ValueError("EMAIL and PASSWORD environment variables must be set")