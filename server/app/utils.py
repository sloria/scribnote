# -*- coding: utf-8 -*-
'''Helper utilities and decorators.'''

from flask.ext.restful import abort as api_abort


def api_get_or_404(model, id, **kwargs):
    return model.query.get(id) or api_abort(404, **kwargs)
