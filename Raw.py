# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 16:11:48 2019

@author: mahir
"""

import tokenize
import operator
import collections
try:
    import StringIO as io
except ImportError:  # pragma: no cover
    import io


__all__ = ['OP', 'COMMENT', 'TOKEN_NUMBER', 'NL', 'NEWLINE', 'EM', 'Module',
           '_generate', '_fewer_tokens', '_find', '_logical', 'analyze']

COMMENT = tokenize.COMMENT
OP = tokenize.OP
NL = tokenize.NL
NEWLINE = tokenize.NEWLINE
EM = tokenize.ENDMARKER

TOKEN_NUMBER = operator.itemgetter(0)

Module = collections.namedtuple('Module', ['loc', 'lloc', 'sloc',
                                           'comments', 'multi', 'blank',
                                           'single_comments'])


def _generate(code):
    return list(tokenize.generate_tokens(io.StringIO(code).readline))


def _fewer_tokens(tokens, remove):

    for values in tokens:
        if values[0] in remove:
            continue
        yield values


def _find(tokens, token, value):
    for index, token_values in enumerate(reversed(tokens)):
        if (token, value) == token_values[:2]:
            return len(tokens) - index - 1
    raise ValueError('(token, value) pair not found')


def _split_tokens(tokens, token, value):
    res = [[]]
    for token_values in tokens:
        if (token, value) == token_values[:2]:
            res.append([])
            continue
        res[-1].append(token_values)
    return res


def _get_all_tokens(line, lines):

    buffer = line
    used_lines = [line]
    while True:
        try:
            tokens = _generate(buffer)
        except tokenize.TokenError:
            pass
        else:
            if not any(t[0] == tokenize.ERRORTOKEN for t in tokens):
                return tokens, used_lines

        next_line = next(lines)
        buffer = buffer + '\n' + next_line
        used_lines.append(next_line)


def _logical(tokens):

    def aux(sub_tokens):

        processed = list(_fewer_tokens(sub_tokens, [COMMENT, NL, NEWLINE]))
        try:

            token_pos = _find(processed, OP, ':')

            return 2 - (token_pos == len(processed) - 2)
        except ValueError:

            if not list(_fewer_tokens(processed, [NL, NEWLINE, EM])):
                return 0
            return 1
    return sum(aux(sub) for sub in _split_tokens(tokens, OP, ';'))


def is_single_token(token_number, tokens):

    return (TOKEN_NUMBER(tokens[0]) == token_number and
            all(TOKEN_NUMBER(t) in (EM, NL, NEWLINE)
                for t in tokens[1:]))


def analyze(source):

    lloc = comments = single_comments = multi = blank = sloc = 0
    lines = (l.strip() for l in source.splitlines())
    lineno = 1
    for line in lines:
        try:

            tokens, parsed_lines = _get_all_tokens(line, lines)
        except StopIteration:
            raise SyntaxError('SyntaxError at line: {0}'.format(lineno))

        lineno += len(parsed_lines)

        comments += sum(1 for t in tokens
                        if TOKEN_NUMBER(t) == tokenize.COMMENT)

        if is_single_token(tokenize.COMMENT, tokens):
            single_comments += 1

        elif is_single_token(tokenize.STRING, tokens):
            _, _, (start_row, _), (end_row, _), _ = tokens[0]
            if end_row == start_row:

                single_comments += 1
            else:
                multi += sum(1 for l in parsed_lines if l)
                blank += sum(1 for l in parsed_lines if not l)
        else:
            for parsed_line in parsed_lines:
                if parsed_line:
                    sloc += 1
                else:
                    blank += 1

        lloc += _logical(tokens)

    loc = sloc + blank + multi + single_comments
    return Module(loc, lloc, sloc, comments, multi, blank, single_comments)