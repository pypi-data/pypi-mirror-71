import { __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import EventDataSection from 'app/components/events/eventDataSection';
import GuideAnchor from 'app/components/assistant/guideAnchor';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { PlatformContextProvider } from './platformContext';
import BreadCrumbsSearch from './breadcrumbsSearch';
import BreadcrumbTime from './breadcrumbTime';
import BreadcrumbCollapsed from './breadcrumbCollapsed';
import convertBreadcrumbType from './convertBreadcrumbType';
import getBreadcrumbDetails from './getBreadcrumbDetails';
import { BreadcrumbType, BreadcrumbLevelType } from './types';
import { BreadCrumb, BreadCrumbIconWrapper } from './styles';
var MAX_CRUMBS_WHEN_COLLAPSED = 10;
var BreadcrumbsContainer = /** @class */ (function (_super) {
    __extends(BreadcrumbsContainer, _super);
    function BreadcrumbsContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isCollapsed: true,
            searchTerm: '',
            breadcrumbs: [],
            filteredBreadcrumbs: [],
        };
        _this.loadCrumbs = function () {
            var data = _this.props.data;
            var breadcrumbs = data.values;
            // Add the error event as the final (virtual) breadcrumb
            var virtualCrumb = _this.getVirtualCrumb();
            if (virtualCrumb) {
                breadcrumbs = __spread(data.values, [virtualCrumb]);
            }
            _this.setState({
                breadcrumbs: breadcrumbs,
                filteredBreadcrumbs: breadcrumbs,
            });
        };
        _this.moduleToCategory = function (module) {
            if (!module) {
                return undefined;
            }
            var match = module.match(/^.*\/(.*?)(:\d+)/);
            if (!match) {
                return module.split(/./)[0];
            }
            return match[1];
        };
        _this.getVirtualCrumb = function () {
            var event = _this.props.event;
            var exception = event.entries.find(function (entry) { return entry.type === 'exception'; });
            if (!exception && !event.message) {
                return undefined;
            }
            if (exception) {
                var _a = exception.data.values[0], type = _a.type, value = _a.value, mdl = _a.module;
                return {
                    type: BreadcrumbType.ERROR,
                    level: BreadcrumbLevelType.ERROR,
                    category: _this.moduleToCategory(mdl) || 'exception',
                    data: {
                        type: type,
                        value: value,
                    },
                    timestamp: event.dateCreated,
                };
            }
            var levelTag = (event.tags || []).find(function (tag) { return tag.key === 'level'; });
            return {
                type: BreadcrumbType.MESSAGE,
                level: levelTag === null || levelTag === void 0 ? void 0 : levelTag.value,
                category: 'message',
                message: event.message,
                timestamp: event.dateCreated,
            };
        };
        _this.getCollapsedCrumbQuantity = function () {
            var _a = _this.state, isCollapsed = _a.isCollapsed, filteredBreadcrumbs = _a.filteredBreadcrumbs;
            var filteredCollapsedBreadcrumbs = filteredBreadcrumbs;
            if (isCollapsed && filteredCollapsedBreadcrumbs.length > MAX_CRUMBS_WHEN_COLLAPSED) {
                filteredCollapsedBreadcrumbs = filteredCollapsedBreadcrumbs.slice(-MAX_CRUMBS_WHEN_COLLAPSED);
            }
            return {
                filteredCollapsedBreadcrumbs: filteredCollapsedBreadcrumbs,
                collapsedQuantity: filteredBreadcrumbs.length - filteredCollapsedBreadcrumbs.length,
            };
        };
        _this.handleChangeSearchTerm = function (searchTerm) {
            var breadcrumbs = _this.state.breadcrumbs;
            var filteredBreadcrumbs = breadcrumbs.filter(function (item) {
                // return true if any of category, message, or level contain queryValue
                return !!['category', 'message', 'level'].find(function (prop) {
                    var propValue = (item[prop] || '').toLowerCase();
                    return propValue.includes(searchTerm);
                });
            });
            _this.setState({
                searchTerm: searchTerm,
                filteredBreadcrumbs: filteredBreadcrumbs,
            });
        };
        _this.handleCollapseToggle = function () {
            _this.setState(function (prevState) { return ({
                isCollapsed: !prevState.isCollapsed,
            }); });
        };
        _this.handleCleanSearch = function () {
            _this.setState({
                searchTerm: '',
                isCollapsed: true,
            });
        };
        return _this;
    }
    BreadcrumbsContainer.prototype.componentDidMount = function () {
        this.loadCrumbs();
    };
    BreadcrumbsContainer.prototype.render = function () {
        var _a = this.props, event = _a.event, type = _a.type;
        var searchTerm = this.state.searchTerm;
        var _b = this.getCollapsedCrumbQuantity(), collapsedQuantity = _b.collapsedQuantity, filteredCollapsedBreadcrumbs = _b.filteredCollapsedBreadcrumbs;
        return (<EventDataSection type={type} title={<h3>
            <GuideAnchor target="breadcrumbs" position="bottom">
              {t('Breadcrumbs')}
            </GuideAnchor>
          </h3>} actions={<BreadCrumbsSearch searchTerm={searchTerm} onChangeSearchTerm={this.handleChangeSearchTerm} onClearSearchTerm={this.handleCleanSearch}/>} wrapTitle={false}>
        <Content>
          {filteredCollapsedBreadcrumbs.length > 0 ? (<PlatformContextProvider value={{ platform: event.platform }}>
              <BreadCrumbs className="crumbs">
                {collapsedQuantity > 0 && (<BreadcrumbCollapsed onClick={this.handleCollapseToggle} quantity={collapsedQuantity}/>)}
                {filteredCollapsedBreadcrumbs.map(function (crumb, idx) {
            var convertedBreadcrumb = convertBreadcrumbType(crumb);
            var _a = getBreadcrumbDetails(convertedBreadcrumb), color = _a.color, borderColor = _a.borderColor, icon = _a.icon, renderer = _a.renderer;
            return (<BreadCrumb data-test-id="breadcrumb" key={idx} hasError={convertedBreadcrumb.type === BreadcrumbType.MESSAGE ||
                convertedBreadcrumb.type === BreadcrumbType.ERROR}>
                      <BreadCrumbIconWrapper color={color} borderColor={borderColor}>
                        {icon}
                      </BreadCrumbIconWrapper>
                      {renderer}
                      <BreadcrumbTime timestamp={crumb.timestamp}/>
                    </BreadCrumb>);
        })}
              </BreadCrumbs>
            </PlatformContextProvider>) : (<EmptyStateWarning small>
              {t('Sorry, no breadcrumbs match your search query.')}
            </EmptyStateWarning>)}
        </Content>
      </EventDataSection>);
    };
    return BreadcrumbsContainer;
}(React.Component));
export default BreadcrumbsContainer;
var BreadCrumbs = styled('ul')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding-left: 0;\n  list-style: none;\n  margin-bottom: 0;\n"], ["\n  padding-left: 0;\n  list-style: none;\n  margin-bottom: 0;\n"])));
var Content = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  border: 1px solid ", ";\n  border-radius: 3px;\n  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);\n  margin-bottom: ", ";\n"], ["\n  border: 1px solid ", ";\n  border-radius: 3px;\n  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.borderLight; }, space(3));
var templateObject_1, templateObject_2;
//# sourceMappingURL=breadcrumbs.jsx.map