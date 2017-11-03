# mpatch
from gevent import monkey
monkey.patch_all()

from cvi.routes import routes

import hug

router = hug.route.API(__name__)

for m, r, h in routes:
    getattr(router, m)(r)(h)
    pass
