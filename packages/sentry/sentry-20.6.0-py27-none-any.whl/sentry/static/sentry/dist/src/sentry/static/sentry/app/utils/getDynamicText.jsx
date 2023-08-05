/* global process */
// Return a specified "fixed" string when we are in a testing environment
// (more specifically in a PERCY env (e.g. CI))
export default function getDynamicText(_a) {
    var value = _a.value, fixed = _a.fixed;
    return process.env.IS_PERCY || process.env.FIXED_DYNAMIC_CONTENT ? fixed : value;
}
//# sourceMappingURL=getDynamicText.jsx.map