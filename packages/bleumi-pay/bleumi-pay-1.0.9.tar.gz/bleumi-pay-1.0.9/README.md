<img src="./assets/images/BleumiPay.png" height="30">

# Bleumi Pay SDK for Python

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://raw.githubusercontent.com/bleumi/bleumi-pay-sdk-python/master/LICENSE)

The Bleumi Pay SDK helps you integrate Algo, Algorand Standard Asset, Ethereum, ERC-20, RSK, RSK ERC-20 & xDai payments and payouts into your business or application. The SDK bundles [Bleumi Pay API](https://pay.bleumi.com/docs/#introduction) into one SDK to ease implementation and support.

**bleumi-pay-sdk-python** is a Python library that provides an interface between your Python application and [Bleumi Pay API](https://pay.bleumi.com/docs/#introduction). This tutorial covers the basics, including examples, needed to use the SDK.

## Getting Started

### Pre-requisites

#### Development Environment

Python 2.7 and 3.4+

#### Obtain An API Key

Bleumi Pay SDK uses API keys to authenticate requests. You can obtain an API key through the [Bleumi Pay Dashboard](https://pay.bleumi.com/app/).

### Install Package

[![pypi (scoped)](https://img.shields.io/pypi/v/bleumi-pay.svg)](https://pypi.org/project/bleumi-pay/)

To install, use `pip` or `easy_install`:

```bash
pip install --upgrade bleumi-pay
```

or

```bash
easy_install --upgrade bleumi-pay
```

Or you can install directly from Github

```sh
pip install git+https://github.com/bleumi/bleumi-pay-sdk-python.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/bleumi/bleumi-pay-sdk-python.git`)

Then import the package:
```python
import bleumi_pay 
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import bleumi_pay
```

### Run Sample Code

The following code generates an unique checkout URL to accept payment from the buyer:

```python
from __future__ import print_function
import time
import bleumi_pay
from bleumi_pay.rest import ApiException
from pprint import pprint

# Configure API key authorization: ApiKeyAuth
configuration = bleumi_pay.Configuration()
configuration.api_key['x-api-key'] = '<Your API Key>' # Replace <Your API Key> with your actual API key

# create an instance of the API class
api_instance = bleumi_pay.HostedCheckoutsApi(bleumi_pay.ApiClient(configuration))
id = '<ID>' # Eg. "1"
amount = '<AMT>' # Eg. "10"
currency = '<CURRENCY>' # Eg. "USD" / "EUR" / "ALGO" / "ETH" ..
success_url = '<SUCCESS_URL>' # Eg. "https://demo.store/api/completeOrder"
cancel_url = '<CANCEL_URL>' # Eg. "https://demo.store/api/cancelOrder"
# Optionally set the token, chain
token = '<TOKEN>' # str |  Replace <TOKEN>  by anyone of the following values: 'ETH' or 'XDAI' or 'XDAIT' or ECR-20 Contract Address or 'RBTC' or RSK ECR-20 Contract Address or 'Asset ID' of Algorand Standard Asset. | Optional
chain = bleumi_pay.Chain.GOERLI # Replace with any Chain as required

try:
    # CreateCheckoutUrlRequest | Specify checkout URL creation parameters.
    create_checkout_url_request = bleumi_pay.CreateCheckoutUrlRequest(
        id=id, 
        amount=amount, 
        currency=currency, 
        success_url=success_url, 
        cancel_url=cancel_url, 
        token=token,
        chain=chain)
    # Generate a unique checkout URL to accept payment.
    api_response = api_instance.create_checkout_url(create_checkout_url_request)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling create_checkout_url: %s\n" % e)
```

More examples can be found under each method in [SDK Classes](#sdk-classes) section.

## SDK Classes

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
HostedCheckoutsApi | [**create_checkout_url**](docs/HostedCheckoutsApi.md#create_checkout_url) | **POST** /v1/payment/hc | Generate a unique checkout URL to accept payment.
HostedCheckoutsApi | [**list_tokens**](docs/HostedCheckoutsApi.md#list_tokens) | **GET** /v1/payment/hc/tokens | Retrieve all tokens configured for the Hosted Checkout in your account in the [Bleumi Pay Dashboard](https://pay.bleumi.com/app/).
HostedCheckoutsApi | [**validate_checkout_payment**](docs/HostedCheckoutsApi.md#validate_checkout_payment) | **POST** /v1/payment/hc/validate | Validate the GET parameters passed by Hosted Checkout in successUrl upon successfully completing payment.
PaymentsApi | [**get_payment**](docs/PaymentsApi.md#get_payment) | **GET** /v1/payment/{id} | Retrieve the wallet addresses &amp; token balances for a given payment
PaymentsApi | [**list_payments**](docs/PaymentsApi.md#list_payments) | **GET** /v1/payment | Retrieve all payments created.
PaymentsApi | [**settle_payment**](docs/PaymentsApi.md#settle_payment) | **POST** /v1/payment/{id}/settle | Settle a specific amount of a token for a given payment to the transferAddress and remaining balance (if any) will be refunded to the buyerAddress
PaymentsApi | [**refund_payment**](docs/PaymentsApi.md#refund_payment) | **POST** /v1/payment/{id}/refund | Refund the balance of a token for a given payment to the buyerAddress
PaymentsApi | [**get_payment_operation**](docs/PaymentsApi.md#get_payment_operation) | **GET** /v1/payment/{id}/operation/{txid} | Retrieve a payment operation for a specific payment.
PaymentsApi | [**list_payment_operations**](docs/PaymentsApi.md#list_payment_operations) | **GET** /v1/payment/{id}/operation | Retrieve all payment operations for a specific payment.
PayoutsApi | [**create_payout**](docs/PayoutsApi.md#create_payout) | **POST** /v1/payout | Create a payout.
PayoutsApi | [**list_payouts**](docs/PayoutsApi.md#list_payouts) | **GET** /v1/payout | Returns a list of payouts

## Documentation For Models

 - [AlgorandAddress](docs/AlgorandAddress.md)
 - [AlgorandBalance](docs/AlgorandBalance.md) 
 - [AlgorandWalletAddress](docs/AlgorandWalletAddress.md)
 - [AlgorandWalletInputs](docs/AlgorandWalletInputs.md) 
 - [BadRequest](docs/BadRequest.md)
 - [Chain](docs/Chain.md)
 - [CheckoutToken](docs/CheckoutToken.md)
 - [CreateCheckoutUrlRequest](docs/CreateCheckoutUrlRequest.md)
 - [CreateCheckoutUrlResponse](docs/CreateCheckoutUrlResponse.md)
 - [CreatePayoutRequest](docs/CreatePayoutRequest.md)
 - [CreatePayoutResponse](docs/CreatePayoutResponse.md)
 - [EthereumAddress](docs/EthereumAddress.md)
 - [EthereumBalance](docs/EthereumBalance.md)
 - [EthereumWalletAddress](docs/EthereumWalletAddress.md)
 - [EthereumWalletInputs](docs/EthereumWalletInputs.md) 
 - [PaginatedPaymentOperations](docs/PaginatedPaymentOperations.md)
 - [PaginatedPayments](docs/PaginatedPayments.md)
 - [PaginatedPayoutItems](docs/PaginatedPayoutItems.md)
 - [Payment](docs/Payment.md)
 - [PaymentAddresses](docs/PaymentAddresses.md)
 - [PaymentBalances](docs/PaymentBalances.md)
 - [PaymentOperation](docs/PaymentOperation.md)
 - [PaymentOperationInputs](docs/PaymentOperationInputs.md)
 - [PaymentOperationResponse](docs/PaymentOperationResponse.md)
 - [PaymentRefundRequest](docs/PaymentRefundRequest.md)
 - [PaymentSettleRequest](docs/PaymentSettleRequest.md)
 - [Payout](docs/Payout.md)
 - [PayoutItem](docs/PayoutItem.md)
 - [PayoutItemInputs](docs/PayoutItemInputs.md)
 - [RskAddress](docs/RskAddress.md)
 - [RskBalance](docs/RskBalance.md)
 - [ValidateCheckoutRequest](docs/ValidateCheckoutRequest.md)
 - [ValidateCheckoutResponse](docs/ValidateCheckoutResponse.md)
 - [WalletBalance](docs/WalletBalance.md)

## Limitations

 - [Bleumi Pay API Limits](https://pay.bleumi.com/docs/#api-limits)

## Recommendation

It's recommended to create an instance of `ApiClient` per thread in a multi-threaded environment to avoid any potential issues.

## License

Copyright 2020 Bleumi, Inc.

Code licensed under the [MIT License](LICENSE).