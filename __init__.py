
from flask import Flask

app = Flask(__name__)

examples = [
    ('http://www.latimes.com/business/autos/la-fi-hy-toyota-honda-fail-iihs-crash-tests-20140121,0,2230299.story',
     'Small car crashes'),
    ('http://bleacherreport.com/articles/1931210-warren-buffet-will-pay-1-billion-to-fan-with-perfect-march-madness-bracket',
     '$1 billion prediction'),
    ('http://www.techtimes.com/articles/2897/20140123/archaeologists-stumped-by-discovery-of-3600-year-old-pharaoh-woseribre-senebkay-tomb.htm',
     'New mummy'),
    ]

import NewsSpectrum.views
