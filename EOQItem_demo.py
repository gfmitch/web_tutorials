#%% Sample program illustrating the use of EOQ Item

from EOQItem import ErrorEOQ
from EOQItem import EOQItem

# create a valid EOQItem

print('Creating our first EOQItem instance.')
item = EOQItem(10000, 500, 12.95, 0.35)
print(item)
print(item.eoq())
print(item.recalc_needed)
print(item.trc())
print(item.atc())

rslt = item.order_policy()
print(rslt)

#%% Illustrate an attempt to create an invalid EOQ item. The try/except is necessary here because we know the
#   constructor is going to throw an exception. In fact, whenever a method can potentially throw an exception, we should
#   wrap the call in a try/except.

print('\n\nAttempting to create an item with an invalid model parameter')
try:
    item_bad = EOQItem(10000, 0, 12.95, 0.35)
    print(f'Item successfully created: \n{item}')
except ErrorEOQ as e:
    # The constructor threw an exception, preventing construction of an invalid EOQItem object.
    print(e.msg)

#%% Let's simulate some inventory activity

print('\n\nInitializing on hand inventory for the valid EOQItem.')
# first, we'll place an order for the EOQ
item.increase_oo(round(item.eoq()))

# Then we'll add a beginning oh balance (i.e., as if remaining from a previous order)
item.increase_oh(500)

print(item)

#%% Now we'll simulate some order activity for 10 days

print('\n\nSimulating daily demand realization for the valid EOQItem assuming constant demand.')
daily_dmd = round(item.d / 262)

for i in range(1,11):
    boh = item.oh
    eoh = item.decrease_oh(daily_dmd)
    print(f'Day {i}: boh - daily_dmd = {boh} - {daily_dmd} = {eoh}')

#%% Here's an example of managing inventory for 5 items. The items do all of the work, we just have to be aware
#   of the items.

# construct an empty list
items = []

# add new EOQItems to the list. Index into the list is the "item id"

items.append(EOQItem(10000, 500, 12.95, 0.35))
items.append(EOQItem(500, 500, 617.98, 0.25))
items.append(EOQItem(1000, 2500, 1500.00, 0.35))
items.append(EOQItem(1000, 2500, 125.95, 0.21))
items.append(EOQItem(47, 125, 2.95, 0.35))

print('\n\nBefore initializing inventory\n')
for item in items:
  print(f'{item}\n')

# initialize on hand inventory for all 5 items, set to EOQ

print('\n\nAfter initializing inventory\n')
for item in items:
    item.increase_oh(round(item.eoq()))
    print(f'{item}\n')

# process sales transactions (i.e., decrement inventory). tuple input is (item id, sale qty)

print('\n\nProcessing sales transactions for the 5 EOQItems')
transactions = [(3, 5),
                (0, 25),
                (3, 1),
                (1, 17),
                (4, 1),
                (2, 12),
                (0, 13),
                (0, 1),
                (2, 1),
                (4, 3)
                ]

for t in transactions:
    id, qty = t

    boh = items[id].oh

    # decrease_oh returns the new oh value, so we save and use in output
    eoh = items[id].decrease_oh(qty)

    print(f'Item {id}: boh={boh}, qty={qty}, eoh={eoh}')

