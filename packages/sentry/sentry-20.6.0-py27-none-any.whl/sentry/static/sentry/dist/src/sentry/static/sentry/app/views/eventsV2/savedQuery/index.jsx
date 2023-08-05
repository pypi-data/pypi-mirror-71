import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { browserHistory } from 'react-router';
import { t } from 'app/locale';
import withApi from 'app/utils/withApi';
import Button from 'app/components/button';
import DropdownButton from 'app/components/dropdownButton';
import DropdownControl from 'app/components/dropdownControl';
import Input from 'app/components/forms/input';
import space from 'app/styles/space';
import { IconBookmark, IconDelete } from 'app/icons';
import EventView from 'app/utils/discover/eventView';
import { getDiscoverLandingUrl } from '../utils';
import { handleCreateQuery, handleUpdateQuery, handleDeleteQuery } from './utils';
var SavedQueryButtonGroup = /** @class */ (function (_super) {
    __extends(SavedQueryButtonGroup, _super);
    function SavedQueryButtonGroup() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isNewQuery: true,
            isEditingQuery: false,
            queryName: '',
        };
        _this.onBlurInput = function (event) {
            var target = event.target;
            _this.setState({ queryName: target.value });
        };
        _this.onChangeInput = function (event) {
            var target = event.target;
            _this.setState({ queryName: target.value });
        };
        /**
         * There are two ways to create a query
         * 1) Creating a query from scratch and saving it
         * 2) Modifying an existing query and saving it
         */
        _this.handleCreateQuery = function (event) {
            event.preventDefault();
            event.stopPropagation();
            var _a = _this.props, api = _a.api, organization = _a.organization, eventView = _a.eventView;
            if (!_this.state.queryName) {
                return;
            }
            var nextEventView = eventView.clone();
            nextEventView.name = _this.state.queryName;
            // Checks if "Save as" button is clicked from a clean state, or it is
            // clicked while modifying an existing query
            var isNewQuery = !eventView.id;
            handleCreateQuery(api, organization, nextEventView, isNewQuery).then(function (savedQuery) {
                var view = EventView.fromSavedQuery(savedQuery);
                _this.setState({ queryName: '' });
                browserHistory.push(view.getResultsViewUrlTarget(organization.slug));
            });
        };
        _this.handleUpdateQuery = function (event) {
            event.preventDefault();
            event.stopPropagation();
            var _a = _this.props, api = _a.api, organization = _a.organization, eventView = _a.eventView;
            handleUpdateQuery(api, organization, eventView).then(function (savedQuery) {
                var view = EventView.fromSavedQuery(savedQuery);
                _this.setState({ queryName: '' });
                browserHistory.push(view.getResultsViewUrlTarget(organization.slug));
            });
        };
        _this.handleDeleteQuery = function (event) {
            event.preventDefault();
            event.stopPropagation();
            var _a = _this.props, api = _a.api, organization = _a.organization, eventView = _a.eventView;
            handleDeleteQuery(api, organization, eventView).then(function () {
                browserHistory.push({
                    pathname: getDiscoverLandingUrl(organization),
                    query: {},
                });
            });
        };
        return _this;
    }
    SavedQueryButtonGroup.getDerivedStateFromProps = function (nextProps, prevState) {
        var nextEventView = nextProps.eventView, savedQuery = nextProps.savedQuery, savedQueryLoading = nextProps.savedQueryLoading;
        // For a new unsaved query
        if (!savedQuery) {
            return {
                isNewQuery: true,
                isEditingQuery: false,
                queryName: prevState.queryName || '',
            };
        }
        if (savedQueryLoading) {
            return prevState;
        }
        var savedEventView = EventView.fromSavedQuery(savedQuery);
        // Switching from a SavedQuery to another SavedQuery
        if (savedEventView.id !== nextEventView.id) {
            return {
                isNewQuery: false,
                isEditingQuery: false,
                queryName: '',
            };
        }
        // For modifying a SavedQuery
        var isEqualQuery = nextEventView.isEqualTo(savedEventView);
        return {
            isNewQuery: false,
            isEditingQuery: !isEqualQuery,
            // HACK(leedongwei): See comment at SavedQueryButtonGroup.onFocusInput
            queryName: prevState.queryName || '',
        };
    };
    SavedQueryButtonGroup.prototype.renderButtonSaveAs = function () {
        var disabled = this.props.disabled;
        var _a = this.state, isNewQuery = _a.isNewQuery, isEditingQuery = _a.isEditingQuery, queryName = _a.queryName;
        if (!isNewQuery && !isEditingQuery) {
            return null;
        }
        /**
         * For a great UX, we should focus on `ButtonSaveInput` when `ButtonSave`
         * is clicked. However, `DropdownControl` wraps them in a FunctionComponent
         * which breaks `React.createRef`.
         */
        return (<DropdownControl alignRight menuWidth="220px" button={function (_a) {
            var isOpen = _a.isOpen, getActorProps = _a.getActorProps;
            return (<ButtonSaveAs data-test-id="button-save-as" {...getActorProps()} isOpen={isOpen} showChevron={false} disabled={disabled}>
            <StyledIconBookmark size="xs" color="gray500"/>
            {t('Save as...')}
          </ButtonSaveAs>);
        }}>
        <ButtonSaveDropDown onClick={SavedQueryButtonGroup.stopEventPropagation}>
          <ButtonSaveInput type="text" name="query_name" placeholder={t('Display name')} value={queryName || ''} onBlur={this.onBlurInput} onChange={this.onChangeInput} disabled={disabled}/>
          <Button data-test-id="button-save-query" onClick={this.handleCreateQuery} priority="primary" disabled={disabled || !this.state.queryName} style={{ width: '100%' }}>
            {t('Save')}
          </Button>
        </ButtonSaveDropDown>
      </DropdownControl>);
    };
    SavedQueryButtonGroup.prototype.renderButtonSaved = function () {
        var _a = this.state, isNewQuery = _a.isNewQuery, isEditingQuery = _a.isEditingQuery;
        if (isNewQuery || isEditingQuery) {
            return null;
        }
        return (<ButtonSaved disabled={this.props.disabled}>
        <StyledIconBookmark isSolid size="xs" color="yellow"/>
        {t('Saved query')}
      </ButtonSaved>);
    };
    SavedQueryButtonGroup.prototype.renderButtonUpdate = function () {
        var _a = this.state, isNewQuery = _a.isNewQuery, isEditingQuery = _a.isEditingQuery;
        if (isNewQuery || !isEditingQuery) {
            return null;
        }
        return (<Button onClick={this.handleUpdateQuery} data-test-id="discover2-savedquery-button-update" disabled={this.props.disabled}>
        <IconUpdate />
        {t('Update query')}
      </Button>);
    };
    SavedQueryButtonGroup.prototype.renderButtonDelete = function () {
        var isNewQuery = this.state.isNewQuery;
        if (isNewQuery) {
            return null;
        }
        return (<Button data-test-id="discover2-savedquery-button-delete" onClick={this.handleDeleteQuery} disabled={this.props.disabled} icon={<IconDelete />}/>);
    };
    SavedQueryButtonGroup.prototype.render = function () {
        return (<ButtonGroup>
        {this.renderButtonDelete()}
        {this.renderButtonSaveAs()}
        {this.renderButtonUpdate()}
        {this.renderButtonSaved()}
      </ButtonGroup>);
    };
    /**
     * Stop propagation for the input and container so people can interact with
     * the inputs in the dropdown.
     */
    SavedQueryButtonGroup.stopEventPropagation = function (event) {
        var capturedElements = ['LI', 'INPUT'];
        if (event.target instanceof Element &&
            capturedElements.includes(event.target.nodeName)) {
            event.preventDefault();
            event.stopPropagation();
        }
    };
    SavedQueryButtonGroup.defaultProps = {
        disabled: false,
    };
    return SavedQueryButtonGroup;
}(React.PureComponent));
var ButtonGroup = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin-top: ", ";\n\n  > * + * {\n    margin-left: ", ";\n  }\n\n  @media (min-width: ", ") {\n    margin-top: 0;\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  margin-top: ", ";\n\n  > * + * {\n    margin-left: ", ";\n  }\n\n  @media (min-width: ", ") {\n    margin-top: 0;\n  }\n"])), space(1), space(1), function (p) { return p.theme.breakpoints[1]; });
var ButtonSaveAs = styled(DropdownButton)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  z-index: ", ";\n  white-space: nowrap;\n"], ["\n  z-index: ", ";\n  white-space: nowrap;\n"])), function (p) { return p.theme.zIndex.dropdownAutocomplete.actor; });
var ButtonSaved = styled(Button)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  cursor: not-allowed;\n"], ["\n  cursor: not-allowed;\n"])));
var ButtonSaveDropDown = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  padding: ", ";\n"], ["\n  padding: ", ";\n"])), space(1));
var ButtonSaveInput = styled(Input)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  width: 100%;\n  margin-bottom: ", ";\n"], ["\n  width: 100%;\n  margin-bottom: ", ";\n"])), space(1));
var StyledIconBookmark = styled(IconBookmark)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(1));
var IconUpdate = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  display: inline-block;\n  width: 10px;\n  height: 10px;\n\n  margin-right: ", ";\n  border-radius: 5px;\n  background-color: ", ";\n"], ["\n  display: inline-block;\n  width: 10px;\n  height: 10px;\n\n  margin-right: ", ";\n  border-radius: 5px;\n  background-color: ", ";\n"])), space(0.75), function (p) { return p.theme.yellow; });
export default withApi(SavedQueryButtonGroup);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=index.jsx.map