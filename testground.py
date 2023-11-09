# File to test quick snippets
import shelve

s = shelve.open('test_shelf.db')
try:
    s['key1'] = { 'int': 10, 'float':9.5, 'string':'Sample data' }
finally:
    s.close()

existing = []
s = shelve.open('test_shelf.db')
try:
    existing = s['key1']
finally:
    s.close()

print(existing)