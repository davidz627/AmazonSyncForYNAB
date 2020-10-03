# Amazon For YNAB

## Context & Purpose

Amazon transactions show up in YNAB as "Amazon.com" in YNAB with no further description by default. This makes it difficult to categorize and understand historical transactions as they have no indication of the item purchased.

The purpose of this project is to reconcile Amazon order item data into the memo of your YNAB transactions.

## Setup & Usage

### Installing Requirements

`pip3 install -r requirements.txt`

### Adding Credentials

You will need to add your personal credentials in a file relative to the project root:
`{root}/secrets/credentials.ini`

The file should have the format:
`
[DEFAULT]
otpSecret={otpSecret}
userEmail=foo@bar.com
userPassword=mySecurePasswordInPlaintextLol
ynabToken=mySecureTokenInPlaintextHaha
`

otpSecret is only required if your Amazon account is protected by OTP. To get this secret you can go to the OTP setup page and set up TFA, scan the QR code with a generic QR Code Reader - the returned data string contains your OTP secret.

### Running

`python3 main.py`

## Contributing

Contributions are welcome. Please create a pull request with an adequate description of your change.


## License

GNU GPLv3

I kind of just picked this as a safe option. Let me know if you have a recommendation to change the license with a succinct reasoning.