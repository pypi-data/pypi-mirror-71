import { __extends, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import InlineSvg from 'app/components/inlineSvg';
import Tooltip from 'app/components/tooltip';
import { t, tn } from 'app/locale';
var REMARKS = {
    a: 'Annotated',
    x: 'Removed',
    s: 'Replaced',
    m: 'Masked',
    p: 'Pseudonymized',
    e: 'Encrypted',
};
var KNOWN_RULES = {
    '!limit': 'size limits',
    '!raw': 'raw payload',
    '!config': 'SDK configuration',
};
function getTooltipText(remark, rule) {
    var remark_title = REMARKS[remark];
    var rule_title = KNOWN_RULES[rule] || t('PII rule "%s"', rule);
    if (remark_title) {
        return t('%s because of %s', remark_title, rule_title);
    }
    else {
        return rule_title;
    }
}
function renderChunk(chunk) {
    if (chunk.type === 'redaction') {
        var title = getTooltipText(chunk.remark, chunk.rule_id);
        return (<Tooltip title={title}>
        <Redaction>{chunk.text}</Redaction>
      </Tooltip>);
    }
    return <span>{chunk.text}</span>;
}
function renderChunks(chunks) {
    var spans = chunks.map(function (chunk, key) { return React.cloneElement(renderChunk(chunk), { key: key }); });
    return <ChunksSpan>{spans}</ChunksSpan>;
}
function renderValue(value, meta) {
    var _a, _b, _c, _d;
    if (((_a = meta === null || meta === void 0 ? void 0 : meta.chunks) === null || _a === void 0 ? void 0 : _a.length) && meta.chunks.length > 1) {
        return renderChunks(meta.chunks);
    }
    var element = value;
    if (value && meta) {
        element = <Redaction>{value}</Redaction>;
    }
    else if ((_b = meta === null || meta === void 0 ? void 0 : meta.err) === null || _b === void 0 ? void 0 : _b.length) {
        element = <Placeholder>invalid</Placeholder>;
    }
    else if ((_c = meta === null || meta === void 0 ? void 0 : meta.rem) === null || _c === void 0 ? void 0 : _c.length) {
        element = <Placeholder>redacted</Placeholder>;
    }
    if ((_d = meta === null || meta === void 0 ? void 0 : meta.rem) === null || _d === void 0 ? void 0 : _d.length) {
        var title = getTooltipText(meta.rem[0][1], meta.rem[0][0]);
        element = <Tooltip title={title}>{element}</Tooltip>;
    }
    return element;
}
function getErrorMessage(error) {
    var errorMessage = [];
    if (error[0]) {
        errorMessage.push(error[0]);
    }
    if (error[1] && error[1].reason) {
        errorMessage.push(error[1].reason);
    }
    return errorMessage.join(': ');
}
function renderErrors(errors) {
    if (!errors.length) {
        return null;
    }
    var tooltip = (<div style={{ textAlign: 'left' }}>
      <strong>{tn('Processing Error:', 'Processing Errors:', errors.length)}</strong>
      <ul>
        {errors.map(function (error, index) { return (<li key={index}>{getErrorMessage(error)}</li>); })}
      </ul>
    </div>);
    return (<Tooltip title={tooltip}>
      <ErrorIcon src="icon-circle-exclamation"/>
    </Tooltip>);
}
var AnnotatedText = /** @class */ (function (_super) {
    __extends(AnnotatedText, _super);
    function AnnotatedText() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AnnotatedText.prototype.render = function () {
        var _a = this.props, value = _a.value, meta = _a.meta, props = __rest(_a, ["value", "meta"]);
        return (<span {...props}>
        {renderValue(value, meta)}
        {(meta === null || meta === void 0 ? void 0 : meta.err) && renderErrors(meta.err)}
      </span>);
    };
    return AnnotatedText;
}(React.Component));
var ChunksSpan = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  span {\n    display: inline;\n  }\n"], ["\n  span {\n    display: inline;\n  }\n"])));
var Redaction = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  background: rgba(255, 0, 0, 0.05);\n  cursor: default;\n"], ["\n  background: rgba(255, 0, 0, 0.05);\n  cursor: default;\n"])));
var Placeholder = styled(Redaction)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-style: italic;\n\n  :before {\n    content: '<';\n  }\n  :after {\n    content: '>';\n  }\n"], ["\n  font-style: italic;\n\n  :before {\n    content: '<';\n  }\n  :after {\n    content: '>';\n  }\n"])));
var ErrorIcon = styled(InlineSvg)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (props) { return props.theme.redDark; });
export default AnnotatedText;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=annotatedText.jsx.map