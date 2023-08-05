import { __assign, __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import pick from 'lodash/pick';
import omit from 'lodash/omit';
import EventDataSection from 'app/components/events/eventDataSection';
import GuideAnchor from 'app/components/assistant/guideAnchor';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import { t } from 'app/locale';
import space from 'app/styles/space';
import SearchBar from 'app/components/searchBar';
import Button from 'app/components/button';
import { IconWarning } from 'app/icons/iconWarning';
import { defined } from 'app/utils';
import { BreadcrumbType, BreadcrumbLevelType, } from './types';
import transformCrumbs from './transformCrumbs';
import Filter from './filter/filter';
import List from './list';
import Level from './level';
import Icon from './icon';
import { aroundContentStyle } from './styles';
var MAX_CRUMBS_WHEN_COLLAPSED = 10;
var ISO_STRING_DATE_AND_TIME_DIVISION = 10;
var Breadcrumbs = /** @class */ (function (_super) {
    __extends(Breadcrumbs, _super);
    function Breadcrumbs() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            searchTerm: '',
            breadcrumbs: [],
            filteredByFilter: [],
            filteredBySearch: [],
            filterOptions: [[], []],
            displayRelativeTime: false,
        };
        _this.listRef = React.createRef();
        _this.expandCollapsedCrumbs = function () {
            _this.setState(function (prevState) { return ({
                filteredBySearch: prevState.breadcrumbs,
            }); }, function () {
                _this.scrollToTheBottom();
            });
        };
        _this.scrollToTheBottom = function () {
            var _a;
            var element = (_a = _this.listRef) === null || _a === void 0 ? void 0 : _a.current;
            if (!element) {
                return;
            }
            element.scrollTo({
                top: element.scrollHeight,
                left: 0,
            });
        };
        _this.loadBreadcrumbs = function () {
            var data = _this.props.data;
            var breadcrumbs = data.values;
            // Add the error event as the final (virtual) breadcrumb
            var virtualCrumb = _this.getVirtualCrumb(breadcrumbs[0]);
            if (virtualCrumb) {
                breadcrumbs = __spread(breadcrumbs, [virtualCrumb]);
            }
            var tranformedCrumbs = transformCrumbs(breadcrumbs);
            var filterOptions = _this.getFilterOptions(tranformedCrumbs);
            _this.setState({
                breadcrumbs: tranformedCrumbs,
                filteredByFilter: tranformedCrumbs,
                filteredBySearch: _this.getCollapsedBreadcrumbs(tranformedCrumbs),
                filterOptions: filterOptions,
            });
        };
        _this.getCollapsedBreadcrumbs = function (breadcrumbs) {
            return breadcrumbs.length > MAX_CRUMBS_WHEN_COLLAPSED
                ? breadcrumbs.slice(-MAX_CRUMBS_WHEN_COLLAPSED)
                : breadcrumbs;
        };
        _this.getFilterOptions = function (breadcrumbs) {
            var types = _this.getFilterTypes(breadcrumbs);
            var levels = _this.getFilterLevels(types);
            return [types, levels];
        };
        _this.getFilterTypes = function (breadcrumbs) {
            var filterTypes = [];
            var _loop_1 = function (index) {
                var breadcrumb = breadcrumbs[index];
                var foundFilterType = filterTypes.findIndex(function (f) { return f.type === breadcrumb.type; });
                if (foundFilterType === -1) {
                    filterTypes.push({
                        type: breadcrumb.type,
                        description: breadcrumb.description,
                        symbol: <Icon {...omit(breadcrumb, 'description')} size="xs"/>,
                        levels: (breadcrumb === null || breadcrumb === void 0 ? void 0 : breadcrumb.level) ? [breadcrumb.level] : [],
                        isChecked: true,
                        isDisabled: false,
                    });
                    return "continue";
                }
                if ((breadcrumb === null || breadcrumb === void 0 ? void 0 : breadcrumb.level) &&
                    !filterTypes[foundFilterType].levels.includes(breadcrumb.level)) {
                    filterTypes[foundFilterType].levels.push(breadcrumb.level);
                }
            };
            for (var index in breadcrumbs) {
                _loop_1(index);
            }
            return filterTypes;
        };
        _this.getFilterLevels = function (types) {
            var filterLevels = [];
            for (var indexType in types) {
                var _loop_2 = function (indexLevel) {
                    var level = types[indexType].levels[indexLevel];
                    if (filterLevels.some(function (f) { return f.type === level; })) {
                        return "continue";
                    }
                    filterLevels.push({
                        type: level,
                        symbol: <Level level={level}/>,
                        isChecked: true,
                        isDisabled: false,
                    });
                };
                for (var indexLevel in types[indexType].levels) {
                    _loop_2(indexLevel);
                }
            }
            return filterLevels;
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
        _this.getVirtualCrumb = function (breadcrumb) {
            var event = _this.props.event;
            var timestamp = (breadcrumb === null || breadcrumb === void 0 ? void 0 : breadcrumb.timestamp) && event.dateCreated
                ? "" + breadcrumb.timestamp.slice(0, ISO_STRING_DATE_AND_TIME_DIVISION) + event.dateCreated.slice(ISO_STRING_DATE_AND_TIME_DIVISION)
                : undefined;
            var exception = event.entries.find(function (entry) { return entry.type === BreadcrumbType.EXCEPTION; });
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
                    timestamp: timestamp,
                };
            }
            var levelTag = (event.tags || []).find(function (tag) { return tag.key === 'level'; });
            return {
                type: BreadcrumbType.ERROR,
                level: levelTag === null || levelTag === void 0 ? void 0 : levelTag.value,
                category: 'message',
                message: event.message,
                timestamp: timestamp,
            };
        };
        _this.filterBySearch = function (searchTerm, breadcrumbs) {
            return !searchTerm.trim()
                ? breadcrumbs
                : breadcrumbs.filter(function (obj) {
                    return Object.keys(pick(obj, ['type', 'category', 'message', 'level', 'timestamp', 'data'])).some(function (key) {
                        if (!defined(obj[key]) || !String(obj[key]).trim()) {
                            return false;
                        }
                        return JSON.stringify(obj[key])
                            .toLocaleLowerCase()
                            .includes(searchTerm);
                    });
                });
        };
        _this.handleSearch = function (value) {
            _this.setState(function (prevState) { return ({
                searchTerm: value,
                filteredBySearch: _this.filterBySearch(value, prevState.filteredByFilter),
            }); });
        };
        _this.handleCleanSearch = function () {
            _this.setState({
                searchTerm: '',
            });
        };
        _this.handleResetFilter = function () {
            _this.handleClickFilterCheckAll(true);
        };
        _this.handleClickFilterCheckAll = function (checkAll) {
            var breadcrumbs = _this.state.breadcrumbs;
            var filteredByFilter = checkAll ? breadcrumbs : [];
            _this.setState(function (prevState) { return ({
                filteredByFilter: filteredByFilter,
                filterOptions: prevState.filterOptions.map(function (filterOption) {
                    return filterOption.map(function (option) { return (__assign(__assign({}, option), { isChecked: checkAll, isDisabled: false })); });
                }),
                filteredBySearch: _this.filterBySearch(prevState.searchTerm, filteredByFilter),
            }); });
        };
        _this.filterCrumbsBy = function (type, breadcrumbs, filterOptions) {
            return breadcrumbs.filter(function (b) {
                var crumbProperty = b[type];
                if (!crumbProperty) {
                    return true;
                }
                var foundInFilterOptions = filterOptions.find(function (f) { return f.type === crumbProperty; });
                if (foundInFilterOptions) {
                    return foundInFilterOptions.isChecked;
                }
                return true;
            });
        };
        _this.handleFilter = function (filterOptions) {
            var breadcrumbs = _this.state.breadcrumbs;
            var filteredCrumbsByType = _this.filterCrumbsBy('type', breadcrumbs, filterOptions[0]);
            var filteredCrumbsByLevel = _this.filterCrumbsBy('level', filteredCrumbsByType, filterOptions[1]);
            _this.setState(function (prevState) { return ({
                filterOptions: filterOptions,
                filteredByFilter: filteredCrumbsByLevel,
                filteredBySearch: _this.filterBySearch(prevState.searchTerm, filteredCrumbsByLevel),
            }); });
        };
        _this.handleSwitchTimeFormat = function () {
            _this.setState(function (prevState) { return ({
                displayRelativeTime: !prevState.displayRelativeTime,
            }); });
        };
        return _this;
    }
    Breadcrumbs.prototype.componentDidMount = function () {
        this.loadBreadcrumbs();
    };
    Breadcrumbs.prototype.componentDidUpdate = function (_prevProps, prevState) {
        if (prevState.breadcrumbs.length === 0 &&
            this.state.breadcrumbs.length >= MAX_CRUMBS_WHEN_COLLAPSED) {
            this.expandCollapsedCrumbs();
        }
    };
    Breadcrumbs.prototype.render = function () {
        var _a = this.props, type = _a.type, event = _a.event, orgId = _a.orgId;
        var _b = this.state, filterOptions = _b.filterOptions, searchTerm = _b.searchTerm, filteredBySearch = _b.filteredBySearch, displayRelativeTime = _b.displayRelativeTime;
        return (<StyledEventDataSection type={type} title={<GuideAnchor target="breadcrumbs" position="bottom">
            <h3>{t('Breadcrumbs')}</h3>
          </GuideAnchor>} actions={<Search>
            <Filter onCheckAll={this.handleClickFilterCheckAll} onFilter={this.handleFilter} options={filterOptions}/>
            <StyledSearchBar placeholder={t('Search breadcrumbs\u2026')} onChange={this.handleSearch} query={searchTerm}/>
          </Search>} wrapTitle={false} isCentered>
        {filteredBySearch.length > 0 ? (<List breadcrumbs={filteredBySearch} ref={this.listRef} event={event} orgId={orgId} onSwitchTimeFormat={this.handleSwitchTimeFormat} displayRelativeTime={displayRelativeTime}/>) : (<StyledEmptyMessage icon={<IconWarning size="xl"/>} action={<Button onClick={this.handleResetFilter} priority="primary">
                {t('Reset Filter')}
              </Button>}>
            {t('Sorry, no breadcrumbs match your search query.')}
          </StyledEmptyMessage>)}
      </StyledEventDataSection>);
    };
    return Breadcrumbs;
}(React.Component));
export default Breadcrumbs;
var StyledEventDataSection = styled(EventDataSection)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(3));
var StyledEmptyMessage = styled(EmptyMessage)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), aroundContentStyle);
var Search = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  width: 100%;\n  margin-top: ", ";\n\n  @media (min-width: ", ") {\n    width: 400px;\n    margin-top: 0;\n  }\n\n  @media (min-width: ", ") {\n    width: 600px;\n  }\n"], ["\n  display: flex;\n  width: 100%;\n  margin-top: ", ";\n\n  @media (min-width: ", ") {\n    width: 400px;\n    margin-top: 0;\n  }\n\n  @media (min-width: ", ") {\n    width: 600px;\n  }\n"])), space(1), function (props) { return props.theme.breakpoints[1]; }, function (props) { return props.theme.breakpoints[3]; });
var StyledSearchBar = styled(SearchBar)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  width: 100%;\n  .search-input {\n    height: 32px;\n  }\n  .search-input,\n  .search-input:focus {\n    border-top-left-radius: 0;\n    border-bottom-left-radius: 0;\n  }\n  .search-clear-form,\n  .icon-search {\n    top: 0 !important;\n    height: 32px;\n    display: flex;\n    align-items: center;\n  }\n"], ["\n  width: 100%;\n  .search-input {\n    height: 32px;\n  }\n  .search-input,\n  .search-input:focus {\n    border-top-left-radius: 0;\n    border-bottom-left-radius: 0;\n  }\n  .search-clear-form,\n  .icon-search {\n    top: 0 !important;\n    height: 32px;\n    display: flex;\n    align-items: center;\n  }\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=breadcrumbs.jsx.map