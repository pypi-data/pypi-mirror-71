import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import { t, tct } from 'app/locale';
import Button from 'app/components/button';
// TODO(matej): refactor to reusable component
var clippedHealthRows = /** @class */ (function (_super) {
    __extends(clippedHealthRows, _super);
    function clippedHealthRows() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            collapsed: true,
        };
        _this.reveal = function () {
            _this.setState({ collapsed: false });
        };
        _this.collapse = function () {
            _this.setState({ collapsed: true });
        };
        return _this;
    }
    clippedHealthRows.prototype.render = function () {
        var _this = this;
        var _a = this.props, children = _a.children, maxVisibleItems = _a.maxVisibleItems, fadeHeight = _a.fadeHeight, className = _a.className;
        var collapsed = this.state.collapsed;
        return (<Wrapper className={className}>
        {children.map(function (item, index) {
            if (!collapsed || index < maxVisibleItems) {
                return item;
            }
            if (index === maxVisibleItems) {
                return (<ShowMoreWrapper fadeHeight={fadeHeight} key="show-more">
                <Button onClick={_this.reveal} priority="primary" size="xsmall" data-test-id="show-more">
                  {tct('Show [numberOfFrames] More', {
                    numberOfFrames: children.length - maxVisibleItems,
                })}
                </Button>
              </ShowMoreWrapper>);
            }
            return null;
        })}

        {!collapsed && children.length > maxVisibleItems && (<CollapseWrapper>
            <Button onClick={this.collapse} priority="primary" size="xsmall" data-test-id="collapse">
              {t('Collapse')}
            </Button>
          </CollapseWrapper>)}
      </Wrapper>);
    };
    clippedHealthRows.defaultProps = {
        maxVisibleItems: 5,
        fadeHeight: '40px',
    };
    return clippedHealthRows;
}(React.Component));
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var ShowMoreWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: absolute;\n  left: 0;\n  right: 0;\n  bottom: 0;\n  background-image: linear-gradient(180deg, hsla(0, 0%, 100%, 0.15) 0, #fff);\n  background-repeat: repeat-x;\n  text-align: center;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  border-bottom: ", " solid #fff;\n  border-top: ", " solid transparent;\n  height: ", ";\n"], ["\n  position: absolute;\n  left: 0;\n  right: 0;\n  bottom: 0;\n  background-image: linear-gradient(180deg, hsla(0, 0%, 100%, 0.15) 0, #fff);\n  background-repeat: repeat-x;\n  text-align: center;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  border-bottom: ", " solid #fff;\n  border-top: ", " solid transparent;\n  height: ", ";\n"])), space(1), space(1), function (p) { return p.fadeHeight; });
var CollapseWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  text-align: center;\n  padding: ", " 0 ", " 0;\n"], ["\n  text-align: center;\n  padding: ", " 0 ", " 0;\n"])), space(0.25), space(1));
export default clippedHealthRows;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=clippedHealthRows.jsx.map