# CountOnce_python

Wrapper for the CountOnce API

## Installation

1. Manually
	- Clone the repo
	```
	$ git clone http://github.com/countonce/countonce-python
	$ cd countonce-python
	```
	- Run the setup
	```
	$ python setup.py install
	```
2. With pip
```
$ pip install countonce_python
```

## Usage
```python
from countonce import CountOnce
import asyncio

# initialize the client with your account id and auth token
co_client = CountOnce(
    account_id = '<your account id>',
    auth_token = '<your auth token>'
)

async def main():
	# use the client in a blocking/sync way
	attributes = {'account_id': 200000, 'actions': 'python'}
	response = await co_client.ping({
		'key': 'account_actions',
		'attributes': attributes,
		'unique_value': 'test'
	})
	print(response.json)

	# use the client in an async way
	key_name = 'account_actions'
	qfilter = {
  		'account_id': 200000,
  		'actions': 'python'
	}
	query_options = {
  		'range': 'last7days',
  		'include': ['current','previous','total'],
  		'filter': qfilter
	}
	# this would return a couroutine that you can 'await' later
	response_2 = co_client.getIncrements(key_name, query_options)
	# ...
	response_json = await response_2
	print(response_json.json)

if __name__ == '__main__':
	asyncio.run(main())

```