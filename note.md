*Rework recipt and order history part - make it with ORM - DONE
*Add recipt number and make that one displayed
*Fix this error that occurs initallty when user not logged in and session has never be loaded:
2025-05-12 13:37:26,508 Unhandled exception during login: 'checkout_redirect'
Traceback (most recent call last):
  File "c:\Users\Dom\Documents\soft_major\Soft_Major\Soft_Major\login_app\login.py", line 93, in form_login
    if session["checkout_redirect"]:
       ~~~~~~~^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Dom\Documents\soft_major\Soft_Major\Soft_Major\env\Lib\site-packages\flask\sessions.py", line 86, in __getitem__
    return super().__getitem__(key)
           ^^^^^^^^^^^^^^^^^^^^^^^^
KeyError: 'checkout_redirect'

See if i can make it so orders 
FIX UP TIME
Error on line 10 in JS still works tho
Fix order date
*Done

Is one example for code optimisation fine?
Find out what this is:
2025-06-04 19:04:14,185 Page not found: /.well-known/appspecific/com.chrome.devtools.json by 127.0.0.1.***Occurs beacuse somehtibg like Chrome DevTools tired acseeing the route which is used to check for debugging or configuration files.
Fix y being not included in box in signup * Done
Find a way to get rid of static/uploads route from get created * Done
See if i can add more than 1 order id in one db entry *Done