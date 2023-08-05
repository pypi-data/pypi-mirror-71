import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { browserHistory } from 'react-router';
import { t } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import withApi from 'app/utils/withApi';
import { addErrorMessage } from 'app/actionCreators/indicator';
import InlineInput from 'app/components/inputInline';
import EventView from 'app/utils/discover/eventView';
import { handleUpdateQueryName } from './savedQuery/utils';
var NAME_DEFAULT = t('Untitled query');
/**
 * Allows user to edit the name of the query. Upon blurring from it, it will
 * save the name change immediately (but not changes in the query)
 */
var EventInputName = /** @class */ (function (_super) {
    __extends(EventInputName, _super);
    function EventInputName() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.refInput = React.createRef();
        _this.onBlur = function (event) {
            var _a = _this.props, api = _a.api, organization = _a.organization, savedQuery = _a.savedQuery, eventView = _a.eventView;
            var nextQueryName = (event.target.value || '').trim();
            // Do not update automatically if
            // 1) New name is empty
            // 2) It is a new query
            // 3) The new name is same as the old name
            if (!nextQueryName) {
                addErrorMessage(t('Please set a name for this query'));
                // Help our users re-focus so they cannot run away from this problem
                if (_this.refInput.current) {
                    _this.refInput.current.focus();
                }
                return;
            }
            if (!savedQuery || savedQuery.name === nextQueryName) {
                return;
            }
            // This ensures that we are updating SavedQuery.name only.
            // Changes on QueryBuilder table will not be saved.
            var nextEventView = EventView.fromSavedQuery(__assign(__assign({}, savedQuery), { name: nextQueryName }));
            handleUpdateQueryName(api, organization, nextEventView).then(function (_updatedQuery) {
                // The current eventview may have changes that are not explicitly saved.
                // So, we just preserve them and change its name
                var renamedEventView = eventView.clone();
                renamedEventView.name = nextQueryName;
                browserHistory.push(renamedEventView.getResultsViewUrlTarget(organization.slug));
            });
        };
        return _this;
    }
    EventInputName.prototype.render = function () {
        var eventView = this.props.eventView;
        return (<StyledListHeader>
        <InlineInput ref={this.refInput} name="discover2-query-name" disabled={!eventView.id} value={eventView.name || NAME_DEFAULT} onBlur={this.onBlur}/>
      </StyledListHeader>);
    };
    return EventInputName;
}(React.Component));
var StyledListHeader = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n  grid-column: 1/2;\n  min-height: 30px;\n  ", ";\n"], ["\n  font-size: ", ";\n  color: ", ";\n  grid-column: 1/2;\n  min-height: 30px;\n  ", ";\n"])), function (p) { return p.theme.headerFontSize; }, function (p) { return p.theme.gray700; }, overflowEllipsis);
export default withApi(EventInputName);
var templateObject_1;
//# sourceMappingURL=eventInputName.jsx.map