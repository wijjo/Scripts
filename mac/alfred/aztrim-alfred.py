# Paste code below into Alfred Run Script action.
import sys
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
url = sys.argv[1]
p = urlparse(url)
url2 = urlunparse((
    p.scheme,
    p.netloc,
    p.path,
    p.params,
    urlencode(
        {k: v for k, v in parse_qsl(p.query)
         if k not in ['qid', 'dc', 'ds', 'crid', 'rnid', 'ref', 'sprefix']}
    ),
    p.fragment,
))
sys.stdout.write(url2)
