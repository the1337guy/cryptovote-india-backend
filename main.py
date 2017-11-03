# mpatch
try:
    from gevent import monkey
    monkey.patch_all()
except Exception:
    pass

from cvi.routes import routes  # noqa

import hug  # noqa

router = hug.route.API(__name__)

for m, r, h in routes:
    getattr(router, m)(r)(h)
    pass
