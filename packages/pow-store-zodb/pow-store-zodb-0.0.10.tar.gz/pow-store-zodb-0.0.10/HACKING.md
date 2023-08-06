# Debugging accidental writes to read-only stores 

The Zope transaction mechanism works by having objects "join" an ongoing
transaction and then responding to calls made by the transaction manager (gory
details available here at the `transaction RTD page <txnrtd>`

txnrtd: https://transaction.readthedocs.io/en/latest/index.html).
