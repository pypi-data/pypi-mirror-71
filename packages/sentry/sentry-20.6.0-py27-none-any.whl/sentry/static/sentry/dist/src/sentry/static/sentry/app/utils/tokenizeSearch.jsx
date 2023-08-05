import { __read, __rest, __spread, __values } from "tslib";
import flatMap from 'lodash/flatMap';
import { escapeDoubleQuotes } from 'app/utils';
/**
 * Tokenize a search into an object
 *
 * Example:
 *   tokenizeSearch('is:resolved foo bar tag:value');
 *   {
 *     is ['resolved'],
 *     query: ['foo', 'bar'],
 *     tag: ['value'],
 *   }
 *
 * Should stay in sync with src.sentry.search.utils:tokenize_query
 */
export function tokenizeSearch(query) {
    var e_1, _a, e_2, _b;
    var tokens = splitSearchIntoTokens(query);
    var searchParams = {
        query: [],
        tags: [],
    };
    try {
        for (var tokens_1 = __values(tokens), tokens_1_1 = tokens_1.next(); !tokens_1_1.done; tokens_1_1 = tokens_1.next()) {
            var token = tokens_1_1.value;
            var tokenState = 'query';
            // Traverse the token and determine if it is a tag
            // condition or bare words.
            for (var i = 0, len = token.length; i < len; i++) {
                var char = token[i];
                if (i === 0 && (char === '"' || char === ':')) {
                    break;
                }
                // We may have entered a tag condition
                if (char === ':') {
                    var nextChar = token[i + 1] || '';
                    if ([':', ' '].includes(nextChar)) {
                        tokenState = 'query';
                    }
                    else {
                        tokenState = 'tags';
                    }
                    break;
                }
            }
            searchParams[tokenState].push(token);
        }
    }
    catch (e_1_1) { e_1 = { error: e_1_1 }; }
    finally {
        try {
            if (tokens_1_1 && !tokens_1_1.done && (_a = tokens_1.return)) _a.call(tokens_1);
        }
        finally { if (e_1) throw e_1.error; }
    }
    var results = {
        query: searchParams.query.map(formatQuery),
    };
    try {
        for (var _c = __values(searchParams.tags), _d = _c.next(); !_d.done; _d = _c.next()) {
            var tag = _d.value;
            var _e = __read(formatTag(tag), 2), key = _e[0], value = _e[1];
            results[key] = Array.isArray(results[key]) ? __spread(results[key], [value]) : [value];
        }
    }
    catch (e_2_1) { e_2 = { error: e_2_1 }; }
    finally {
        try {
            if (_d && !_d.done && (_b = _c.return)) _b.call(_c);
        }
        finally { if (e_2) throw e_2.error; }
    }
    return results;
}
/**
 * Convert a QueryResults object back to a query string
 */
export function stringifyQueryObject(results) {
    var query = results.query, tags = __rest(results, ["query"]);
    var stringTags = flatMap(Object.entries(tags), function (_a) {
        var _b = __read(_a, 2), k = _b[0], values = _b[1];
        return values.map(function (tag) {
            if (tag === '' || tag === null) {
                return k + ":\"\"";
            }
            if (/[\s\(\)\\"]/g.test(tag)) {
                return k + ":\"" + escapeDoubleQuotes(tag) + "\"";
            }
            return k + ":" + tag;
        });
    });
    return (query.join(' ') + " " + stringTags.join(' ')).trim();
}
/**
 * Splits search strings into tokens for parsing by tokenizeSearch.
 */
function splitSearchIntoTokens(query) {
    var queryChars = Array.from(query);
    var tokens = [];
    var token = '';
    var endOfPrevWord = '';
    var quoteType = '';
    var quoteEnclosed = false;
    queryChars.forEach(function (char, idx) {
        var nextChar = queryChars.length - 1 > idx ? queryChars[idx + 1] : null;
        token += char;
        if (nextChar !== null && !isSpace(char) && isSpace(nextChar)) {
            endOfPrevWord = char;
        }
        if (isSpace(char) && !quoteEnclosed && endOfPrevWord !== ':' && !isSpace(token)) {
            tokens.push(token.trim());
            token = '';
        }
        if (["'", '"'].includes(char) && (!quoteEnclosed || quoteType === char)) {
            quoteEnclosed = !quoteEnclosed;
            if (quoteEnclosed) {
                quoteType = char;
            }
        }
    });
    var trimmedToken = token.trim();
    if (trimmedToken !== '') {
        tokens.push(trimmedToken);
    }
    return tokens;
}
/**
 * Checks if the string is only spaces
 */
function isSpace(s) {
    return s.trim() === '';
}
/**
 * Splits tags on ':' and removes enclosing quotes if present, and returns both
 * sides of the split as strings.
 */
function formatTag(tag) {
    var idx = tag.indexOf(':');
    var key = tag.slice(0, idx).replace(/^"+|"+$/g, '');
    var value = tag.slice(idx + 1).replace(/^"+|"+$/g, '');
    return [key, value];
}
/**
 * Strips enclosing quotes from a query, if present.
 */
function formatQuery(query) {
    return query.replace(/^"+|"+$/g, '');
}
//# sourceMappingURL=tokenizeSearch.jsx.map