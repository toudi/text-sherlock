import settings
import linecache
from subprocess import check_output

def extract_lines(_file, query):
    context_lines = settings.NUM_CONTEXT_LINES

    out = []
    used_lines = []
    with open(_file) as input:
        for lineno, line in enumerate(input):
            if query.lower() in unicode(line, 'utf-8').lower():
                for _line in range(lineno - context_lines, lineno + 1 + context_lines):
                    content = linecache.getline(_file, _line+1)
                    if content.strip():
                        if _line not in used_lines:
                            used_lines.append(_line)
                            out.append((_line+1, content))
    return (out, len(str(used_lines[-1])))