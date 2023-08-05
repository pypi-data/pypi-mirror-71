import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { getMeta } from 'app/components/events/meta/metaProxy';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import { defined } from 'app/utils';
import getBreadcrumbCustomRendererValue from '../../breadcrumbs/getBreadcrumbCustomRendererValue';
var Summary = /** @class */ (function (_super) {
    __extends(Summary, _super);
    function Summary() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isExpanded: false,
            hasOverflow: false,
        };
        _this.summaryNode = React.createRef();
        _this.onToggle = function () {
            _this.setState(function (prevState) { return ({
                isExpanded: !prevState.isExpanded,
            }); });
        };
        _this.renderData = function () {
            var kvData = _this.props.kvData;
            if (!kvData) {
                return null;
            }
            return Object.keys(kvData)
                .filter(function (key) { return defined(kvData[key]) && !!kvData[key]; })
                .map(function (key) {
                var value = typeof kvData[key] === 'object' ? JSON.stringify(kvData[key]) : kvData[key];
                return (<Data key={key}>
            <StyledPre>
              <DataLabel>{key + ": "}</DataLabel>
              {getBreadcrumbCustomRendererValue({
                    value: value,
                    meta: getMeta(kvData, key),
                })}
            </StyledPre>
          </Data>);
            });
        };
        return _this;
    }
    // TODO(Priscila): implement Summary lifecycles
    Summary.prototype.render = function () {
        var children = this.props.children;
        return (<React.Fragment>
        <div onClick={this.onToggle} ref={this.summaryNode}>
          <StyledPre>
            <StyledCode>{children}</StyledCode>
          </StyledPre>
        </div>
        {this.renderData()}
      </React.Fragment>);
    };
    return Summary;
}(React.Component));
export default Summary;
var StyledPre = styled('pre')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 0;\n  background: none;\n  box-sizing: border-box;\n  white-space: pre-wrap;\n  word-break: break-all;\n  margin: 0;\n  font-size: ", ";\n  @media (max-width: ", ") {\n    ", ";\n  }\n"], ["\n  padding: 0;\n  background: none;\n  box-sizing: border-box;\n  white-space: pre-wrap;\n  word-break: break-all;\n  margin: 0;\n  font-size: ", ";\n  @media (max-width: ", ") {\n    ", ";\n  }\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.breakpoints[0]; }, overflowEllipsis);
var StyledCode = styled('code')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  white-space: nowrap;\n  @media (min-width: ", ") {\n    white-space: pre-wrap;\n  }\n  line-height: 26px;\n"], ["\n  white-space: nowrap;\n  @media (min-width: ", ") {\n    white-space: pre-wrap;\n  }\n  line-height: 26px;\n"])), function (p) { return p.theme.breakpoints[0]; });
var Data = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; });
var DataLabel = styled('strong')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  line-height: 17px;\n"], ["\n  line-height: 17px;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=summary.jsx.map