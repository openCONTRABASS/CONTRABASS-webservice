Setup Crontab with:

```
crontab -e
```

Executed every two hours:
```
0 0 * * * python3 /home/a718123/CONTRABASS-webservice/scripts/delete_expired_files.py
```
