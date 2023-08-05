import { __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import Tooltip from 'app/components/tooltip';
import InlineSvg from 'app/components/inlineSvg';
import { t } from 'app/locale';
import Tag from 'app/views/settings/components/tag';
var FEATURE_TOOLTIPS = {
    symtab: t('Symbol tables are used as a fallback when full debug information is not available'),
    debug: t('Debug information provides function names and resolves inlined frames during symbolication'),
    unwind: t('Stack unwinding information improves the quality of stack traces extracted from minidumps'),
    sources: t('Source code information allows Sentry to display source code context for stack frames'),
};
var DebugFileFeature = function (_a) {
    var available = _a.available, feature = _a.feature;
    var icon = null;
    if (available === true) {
        icon = <Icon type="success" src="icon-checkmark-sm"/>;
    }
    else if (available === false) {
        icon = <Icon type="error" src="icon-close"/>;
    }
    return (<Tooltip title={FEATURE_TOOLTIPS[feature]}>
      <Tag inline>
        {icon}
        {feature}
      </Tag>
    </Tooltip>);
};
DebugFileFeature.propTypes = {
    available: PropTypes.bool,
    feature: PropTypes.oneOf(Object.keys(FEATURE_TOOLTIPS)).isRequired,
};
var Icon = styled(InlineSvg)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n  margin-right: 1ex;\n"], ["\n  color: ", ";\n  margin-right: 1ex;\n"])), function (p) { return p.theme.alert[p.type].iconColor; });
export default DebugFileFeature;
var templateObject_1;
//# sourceMappingURL=debugFileFeature.jsx.map