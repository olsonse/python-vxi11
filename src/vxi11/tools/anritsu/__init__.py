import re
from ms9740a import MS9740A

models = {
  MS9740A.model : MS9740A,
}

__all__ = [ m.__name__ for m in models.values() ] + ['get']


def get(idn):
  m = re.match('Anritsu,(?P<model>[^,]*),(?P<sn>[^,]*),(?P<fw>[^,]*)', idn)
  if m:
    return models.get(m.group('model').lower(), None)
  return None
