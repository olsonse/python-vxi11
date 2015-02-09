import re
from tds5000b import TDS5000B

models = {
  TDS5000B.model : TDS5000B,
}

__all__ = [ m.__name__ for m in models.values() ] + ['get']


def get(idn):
  m = re.match('tektronix,(?P<model>[^,]*),(?P<sn>[^,]*),(?P<fw>[^,]*)', idn)
  if m:
    return models.get(m.group('model'), None)
  return None
