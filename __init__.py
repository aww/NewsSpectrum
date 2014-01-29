
from flask import Flask

app = Flask(__name__)

examples = [
    ('http://www.nbcnews.com/business/worst-performing-most-minicars-fail-new-frontal-crash-test-2D11968197',                 'Small car crashes'),
    ('http://bleacherreport.com/articles/1931210-warren-buffet-will-pay-1-billion-to-fan-with-perfect-march-madness-bracket', '$1 billion prediction'),
    ('http://www.theverge.com/2014/1/21/5332658/pharaoh-senebkay-mummy-abydos-dynasty',                                       'New mummy'),
    ]

import NewsSpectrum.views
