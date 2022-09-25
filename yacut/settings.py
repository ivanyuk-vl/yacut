import re
from string import ascii_letters, digits

SHORT_ID_CHARS = f'{digits}{ascii_letters}'
SHORT_ID_PATTERN = '^[{}]+$'.format(re.escape(SHORT_ID_CHARS))
MAX_URL_LENGTH = 2048
MAX_SHORT_ID_LENGTH = 16
LIMIT_GENERATE_SHORT_ATTEMTS = 1000
MAX_RANDOM_SHORT_ID_LENGTH = 6
