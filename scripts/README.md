Setup Crontab with:

```
crontab -e
```

Executed every two hours:
```
* */2 * * * python3 delete_expired_files.py
```
