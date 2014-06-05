#joshandre.ws
My personal website, a fork of Americano.

###Nginx setup:
**Start FCGI** spawn-fcgi -d /path/to/www -f /path/to/www/index.py -a 127.0.0.1 -p 8080

**Stop FCGI** kill 'pgrep -f "python /path/to/www/index.py"'
