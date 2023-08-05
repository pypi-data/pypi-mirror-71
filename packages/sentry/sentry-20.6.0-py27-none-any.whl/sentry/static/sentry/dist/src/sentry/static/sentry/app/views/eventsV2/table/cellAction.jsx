import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import ReactDOM from 'react-dom';
import styled from '@emotion/styled';
import { Manager, Reference, Popper } from 'react-popper';
import { t } from 'app/locale';
import { defined } from 'app/utils';
import { IconEllipsis } from 'app/icons';
import space from 'app/styles/space';
import { getAggregateAlias } from 'app/utils/discover/fields';
export var Actions;
(function (Actions) {
    Actions["ADD"] = "add";
    Actions["EXCLUDE"] = "exclude";
    Actions["SHOW_GREATER_THAN"] = "show_greater_than";
    Actions["SHOW_LESS_THAN"] = "show_less_than";
    Actions["TRANSACTION"] = "transaction";
    Actions["RELEASE"] = "release";
    Actions["DRILLDOWN"] = "drilldown";
})(Actions || (Actions = {}));
var CellAction = /** @class */ (function (_super) {
    __extends(CellAction, _super);
    function CellAction(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            isHovering: false,
            isOpen: false,
        };
        _this.handleClickOutside = function (event) {
            if (!_this.menuEl) {
                return;
            }
            if (!(event.target instanceof Element)) {
                return;
            }
            if (_this.menuEl.contains(event.target)) {
                return;
            }
            _this.setState({ isOpen: false, isHovering: false });
        };
        _this.handleMouseEnter = function () {
            _this.setState({ isHovering: true });
        };
        _this.handleMouseLeave = function () {
            _this.setState(function (state) {
                // Don't hide the button if the menu is open.
                if (state.isOpen) {
                    return state;
                }
                return __assign(__assign({}, state), { isHovering: false });
            });
        };
        _this.handleMenuToggle = function (event) {
            event.preventDefault();
            _this.setState({ isOpen: !_this.state.isOpen });
        };
        var portal = document.getElementById('cell-action-portal');
        if (!portal) {
            portal = document.createElement('div');
            portal.setAttribute('id', 'cell-action-portal');
            document.body.appendChild(portal);
        }
        _this.portalEl = portal;
        _this.menuEl = null;
        return _this;
    }
    CellAction.prototype.componentDidUpdate = function (_props, prevState) {
        if (this.state.isOpen && prevState.isOpen === false) {
            document.addEventListener('click', this.handleClickOutside, true);
        }
        if (this.state.isOpen === false && prevState.isOpen) {
            document.removeEventListener('click', this.handleClickOutside, true);
        }
    };
    CellAction.prototype.componentWillUnmount = function () {
        document.removeEventListener('click', this.handleClickOutside, true);
    };
    CellAction.prototype.renderMenuButtons = function () {
        var _a = this.props, dataRow = _a.dataRow, column = _a.column, handleCellAction = _a.handleCellAction, allowActions = _a.allowActions;
        var fieldAlias = getAggregateAlias(column.name);
        var value = dataRow[fieldAlias];
        var actions = [];
        function addMenuItem(action, menuItem) {
            if ((Array.isArray(allowActions) && allowActions.includes(action)) ||
                !allowActions) {
                actions.push(menuItem);
            }
        }
        if (column.type !== 'duration') {
            addMenuItem(Actions.ADD, <ActionItem key="add-to-filter" data-test-id="add-to-filter" onClick={function () { return handleCellAction(Actions.ADD, value); }}>
          {t('Add to filter')}
        </ActionItem>);
            addMenuItem(Actions.EXCLUDE, <ActionItem key="exclude-from-filter" data-test-id="exclude-from-filter" onClick={function () { return handleCellAction(Actions.EXCLUDE, value); }}>
          {t('Exclude from filter')}
        </ActionItem>);
        }
        if (column.type !== 'string' && column.type !== 'boolean') {
            addMenuItem(Actions.SHOW_GREATER_THAN, <ActionItem key="show-values-greater-than" data-test-id="show-values-greater-than" onClick={function () { return handleCellAction(Actions.SHOW_GREATER_THAN, value); }}>
          {t('Show values greater than')}
        </ActionItem>);
            addMenuItem(Actions.SHOW_LESS_THAN, <ActionItem key="show-values-less-than" data-test-id="show-values-less-than" onClick={function () { return handleCellAction(Actions.SHOW_LESS_THAN, value); }}>
          {t('Show values less than')}
        </ActionItem>);
        }
        if (column.column.kind === 'field' && column.column.field === 'transaction') {
            addMenuItem(Actions.TRANSACTION, <ActionItem key="transaction-summary" data-test-id="transaction-summary" onClick={function () { return handleCellAction(Actions.TRANSACTION, value); }}>
          {t('Go to summary')}
        </ActionItem>);
        }
        if (column.column.kind === 'field' && column.column.field === 'release') {
            addMenuItem(Actions.RELEASE, <ActionItem key="release" data-test-id="release" onClick={function () { return handleCellAction(Actions.RELEASE, value); }}>
          {t('Go to release')}
        </ActionItem>);
        }
        if (column.column.kind === 'function' &&
            column.column.function[0] === 'count_unique') {
            addMenuItem(Actions.DRILLDOWN, <ActionItem key="drilldown" data-test-id="per-cell-drilldown" onClick={function () { return handleCellAction(Actions.DRILLDOWN, value); }}>
          {t('View Stacks')}
        </ActionItem>);
        }
        if (actions.length === 0) {
            return null;
        }
        return (<MenuButtons onClick={function (event) {
            // prevent clicks from propagating further
            event.stopPropagation();
        }}>
        {actions}
      </MenuButtons>);
    };
    CellAction.prototype.renderMenu = function () {
        var _this = this;
        var isOpen = this.state.isOpen;
        var menuButtons = this.renderMenuButtons();
        if (menuButtons === null) {
            // do not render the menu if there are no per cell actions
            return null;
        }
        var modifiers = {
            hide: {
                enabled: false,
            },
            preventOverflow: {
                padding: 10,
                enabled: true,
                boundariesElement: 'viewport',
            },
        };
        var menu = null;
        if (isOpen) {
            menu = ReactDOM.createPortal(<Popper placement="top" modifiers={modifiers}>
          {function (_a) {
                var popperRef = _a.ref, style = _a.style, placement = _a.placement, arrowProps = _a.arrowProps;
                return (<Menu ref={function (ref) {
                    popperRef(ref);
                    _this.menuEl = ref;
                }} style={style}>
              <MenuArrow ref={arrowProps.ref} data-placement={placement} style={arrowProps.style}/>
              {menuButtons}
            </Menu>);
            }}
        </Popper>, this.portalEl);
        }
        return (<MenuRoot>
        <Manager>
          <Reference>
            {function (_a) {
            var ref = _a.ref;
            return (<MenuButton ref={ref} onClick={_this.handleMenuToggle}>
                <IconEllipsis size="sm" data-test-id="cell-action" color="blue400"/>
              </MenuButton>);
        }}
          </Reference>
          {menu}
        </Manager>
      </MenuRoot>);
    };
    CellAction.prototype.render = function () {
        var children = this.props.children;
        var isHovering = this.state.isHovering;
        var _a = this.props, dataRow = _a.dataRow, column = _a.column;
        var fieldAlias = getAggregateAlias(column.name);
        var value = dataRow[fieldAlias];
        if (!defined(value)) {
            // per cell actions do not apply to values that are null
            return <React.Fragment>{children}</React.Fragment>;
        }
        return (<Container onMouseEnter={this.handleMouseEnter} onMouseLeave={this.handleMouseLeave}>
        {children}
        {isHovering && this.renderMenu()}
      </Container>);
    };
    return CellAction;
}(React.Component));
export default CellAction;
var Container = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n  width: 100%;\n  height: 100%;\n"], ["\n  position: relative;\n  width: 100%;\n  height: 100%;\n"])));
var MenuRoot = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: absolute;\n  top: 0;\n  right: 0;\n"], ["\n  position: absolute;\n  top: 0;\n  right: 0;\n"])));
var Menu = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin: ", " 0;\n\n  z-index: ", ";\n"], ["\n  margin: ", " 0;\n\n  z-index: ", ";\n"])), space(1), function (p) { return p.theme.zIndex.tooltip; });
var MenuButtons = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  background: ", ";\n  border: 1px solid ", ";\n  border-radius: ", ";\n  box-shadow: ", ";\n  overflow: hidden;\n"], ["\n  background: ", ";\n  border: 1px solid ", ";\n  border-radius: ", ";\n  box-shadow: ", ";\n  overflow: hidden;\n"])), function (p) { return p.theme.white; }, function (p) { return p.theme.borderLight; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.dropShadowHeavy; });
var MenuArrow = styled('span')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  position: absolute;\n  width: 18px;\n  height: 9px;\n  /* left and top set by popper */\n\n  &[data-placement*='bottom'] {\n    margin-top: -9px;\n    &::before {\n      border-width: 0 9px 9px 9px;\n      border-color: transparent transparent ", " transparent;\n    }\n    &::after {\n      top: 1px;\n      left: 1px;\n      border-width: 0 8px 8px 8px;\n      border-color: transparent transparent #fff transparent;\n    }\n  }\n  &[data-placement*='top'] {\n    margin-bottom: -8px;\n    bottom: 0;\n    &::before {\n      border-width: 9px 9px 0 9px;\n      border-color: ", " transparent transparent transparent;\n    }\n    &::after {\n      bottom: 1px;\n      left: 1px;\n      border-width: 8px 8px 0 8px;\n      border-color: #fff transparent transparent transparent;\n    }\n  }\n\n  &::before,\n  &::after {\n    width: 0;\n    height: 0;\n    content: '';\n    display: block;\n    position: absolute;\n    border-style: solid;\n  }\n"], ["\n  position: absolute;\n  width: 18px;\n  height: 9px;\n  /* left and top set by popper */\n\n  &[data-placement*='bottom'] {\n    margin-top: -9px;\n    &::before {\n      border-width: 0 9px 9px 9px;\n      border-color: transparent transparent ", " transparent;\n    }\n    &::after {\n      top: 1px;\n      left: 1px;\n      border-width: 0 8px 8px 8px;\n      border-color: transparent transparent #fff transparent;\n    }\n  }\n  &[data-placement*='top'] {\n    margin-bottom: -8px;\n    bottom: 0;\n    &::before {\n      border-width: 9px 9px 0 9px;\n      border-color: ", " transparent transparent transparent;\n    }\n    &::after {\n      bottom: 1px;\n      left: 1px;\n      border-width: 8px 8px 0 8px;\n      border-color: #fff transparent transparent transparent;\n    }\n  }\n\n  &::before,\n  &::after {\n    width: 0;\n    height: 0;\n    content: '';\n    display: block;\n    position: absolute;\n    border-style: solid;\n  }\n"])), function (p) { return p.theme.borderLight; }, function (p) { return p.theme.borderLight; });
var ActionItem = styled('button')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: block;\n  width: 100%;\n  padding: ", " ", ";\n  background: transparent;\n\n  outline: none;\n  border: 0;\n  border-bottom: 1px solid ", ";\n\n  font-size: ", ";\n  text-align: left;\n  line-height: 1.2;\n\n  &:hover {\n    background: ", ";\n  }\n\n  &:last-child {\n    border-bottom: 0;\n  }\n"], ["\n  display: block;\n  width: 100%;\n  padding: ", " ", ";\n  background: transparent;\n\n  outline: none;\n  border: 0;\n  border-bottom: 1px solid ", ";\n\n  font-size: ", ";\n  text-align: left;\n  line-height: 1.2;\n\n  &:hover {\n    background: ", ";\n  }\n\n  &:last-child {\n    border-bottom: 0;\n  }\n"])), space(1), space(2), function (p) { return p.theme.borderLight; }, function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.gray100; });
var MenuButton = styled('button')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  display: flex;\n  width: 24px;\n  height: 24px;\n  padding: 0;\n  justify-content: center;\n  align-items: center;\n\n  background: rgba(255, 255, 255, 0.85);\n  border-radius: ", ";\n  border: 1px solid ", ";\n  cursor: pointer;\n  outline: none;\n"], ["\n  display: flex;\n  width: 24px;\n  height: 24px;\n  padding: 0;\n  justify-content: center;\n  align-items: center;\n\n  background: rgba(255, 255, 255, 0.85);\n  border-radius: ", ";\n  border: 1px solid ", ";\n  cursor: pointer;\n  outline: none;\n"])), function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.borderLight; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=cellAction.jsx.map