import re
from .mso5074 import MSO5074

models = {
  MSO5074.model : MSO5074,
}

__all__ = [ m.__name__ for m in models.values() ] + ['get']


def get(idn):
  m = re.match('rigol technologies,(?P<model>[^,]*),(?P<sn>[^,]*),(?P<fw>[^,]*)', idn)
  if m:
    return models.get(m.group('model'), None)
  return None
