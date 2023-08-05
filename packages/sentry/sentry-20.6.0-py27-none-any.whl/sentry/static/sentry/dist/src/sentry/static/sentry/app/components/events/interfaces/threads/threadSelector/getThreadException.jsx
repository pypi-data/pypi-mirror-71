import { __values } from "tslib";
function getThreadException(thread, event) {
    var e_1, _a, e_2, _b;
    if (!event || !event.entries) {
        return undefined;
    }
    try {
        for (var _c = __values(event.entries), _d = _c.next(); !_d.done; _d = _c.next()) {
            var entry = _d.value;
            if (entry.type !== 'exception') {
                continue;
            }
            try {
                for (var _e = (e_2 = void 0, __values(entry.data.values)), _f = _e.next(); !_f.done; _f = _e.next()) {
                    var exc = _f.value;
                    if (exc.threadId === thread.id) {
                        return entry.data;
                    }
                }
            }
            catch (e_2_1) { e_2 = { error: e_2_1 }; }
            finally {
                try {
                    if (_f && !_f.done && (_b = _e.return)) _b.call(_e);
                }
                finally { if (e_2) throw e_2.error; }
            }
        }
    }
    catch (e_1_1) { e_1 = { error: e_1_1 }; }
    finally {
        try {
            if (_d && !_d.done && (_a = _c.return)) _a.call(_c);
        }
        finally { if (e_1) throw e_1.error; }
    }
    return undefined;
}
export default getThreadException;
//# sourceMappingURL=getThreadException.jsx.map