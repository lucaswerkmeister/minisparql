#!/usr/bin/env python3

import re
import subprocess
import sys
from urllib.parse import unquote

line = sys.stdin.readline()

(method, path, http) = line.split()

query = re.sub(r'/.*query=([^&]*)(&|$)', r'\1', path)
query = unquote(query)
match = re.search(r'SELECT \(REGEX\(("[^"]*"), ("[^"]*")\) AS \?matches\) {}', query);
if match:
    (text, regex) = match.group(1, 2)
    program = r'''<?php
$match = preg_match('/' . str_replace('/', '\/', $regex) . '/', $text);
if ($match === 1) {
    print('{"results":{"bindings":[{"matches":{"value":"true"}}]}}');
} elseif ($match === 0) {
    print('{"results":{"bindings":[{"matches":{"value":"false"}}]}}');
} else {
    print('{"results":{"bindings":[{}]}}');
}
'''.replace('$text', text).replace('$regex', regex)
    result = subprocess.check_output('php', input=program.encode('UTF-8'))
    print('HTTP/1.1 200 Found\r\n\r\n', end='')
    print(result.decode('UTF-8'))
else:
    print(
        'HTTP/1.1 404 Not found\r'
        '\r',
        sep='\n'
    )
