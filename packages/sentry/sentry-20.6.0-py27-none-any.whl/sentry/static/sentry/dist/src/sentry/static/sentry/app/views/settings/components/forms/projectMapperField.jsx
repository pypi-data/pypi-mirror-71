import { __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { components } from 'react-select';
import InputField from 'app/views/settings/components/forms/inputField';
import SelectControl from 'app/components/forms/selectControl';
import IdBadge from 'app/components/idBadge';
import Button from 'app/components/button';
import { IconAdd } from 'app/icons';
import { t } from 'app/locale';
var RenderField = /** @class */ (function (_super) {
    __extends(RenderField, _super);
    function RenderField() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.sentryProjectRef = React.createRef();
        _this.mappedRef = React.createRef();
        return _this;
    }
    RenderField.prototype.render = function () {
        var _this = this;
        var _a = this.props, onChange = _a.onChange, onBlur = _a.onBlur, value = _a.value, mappedDropdown = _a.mappedDropdown, sentryProjects = _a.sentryProjects, mappedDropdownItems = _a.mappedDropdown.items;
        var existingValues = value || [];
        // create maps by the project id for constant time lookups
        var sentryProjectsById = Object.fromEntries(sentryProjects.map(function (project) { return [project.id, project]; }));
        var mappedItemsByValue = Object.fromEntries(mappedDropdownItems.map(function (item) { return [item.value, item]; }));
        //build sets of values used so we don't let the user select them twice
        var projectIdsUsed = new Set(existingValues.map(function (tuple) { return tuple[0]; }));
        var mappedValuesUsed = new Set(existingValues.map(function (tuple) { return tuple[1]; }));
        var projectOptions = sentryProjects
            .filter(function (project) { return !projectIdsUsed.has(project.id); })
            .map(function (_a) {
            var slug = _a.slug, id = _a.id;
            return ({ label: slug, value: id });
        });
        var mappedItemsToShow = mappedDropdownItems.filter(function (item) { return !mappedValuesUsed.has(item.value); });
        var handleAdd = function () {
            var sentryProjectId = _this.sentryProjectRef.current.state.value.value;
            var mappedValue = _this.mappedRef.current.state.value.value;
            //add the new value to the list of existing values
            var projectMappings = __spread(existingValues, [[sentryProjectId, mappedValue]]);
            //trigger events so we save the value and show the check mark
            onChange === null || onChange === void 0 ? void 0 : onChange(projectMappings, []);
            onBlur === null || onBlur === void 0 ? void 0 : onBlur(projectMappings, []);
        };
        var renderItem = function (itemTuple) {
            var _a = __read(itemTuple, 2), projectId = _a[0], mappedValue = _a[1];
            var slug = sentryProjectsById[projectId].slug;
            var itemLabel = mappedItemsByValue[mappedValue].label;
            return (<Item key={projectId}>
          <ItemValue>{slug}</ItemValue> <ItemValue>{itemLabel}</ItemValue>
        </Item>);
        };
        var customValueContainer = function (containerProps) {
            var valueList = containerProps.getValue();
            //if no value set, we want to return the default component that is rendered
            if (valueList.length === 0) {
                return <components.ValueContainer {...containerProps}/>;
            }
            var projectId = valueList[0].value;
            var project = sentryProjectsById[projectId];
            if (!project) {
                return <components.ValueContainer {...containerProps}/>;
            }
            return (<components.ValueContainer {...containerProps}>
          <IdBadge project={project} avatarSize={20} displayName={project.slug} avatarProps={{ consistentWidth: true }}/>
        </components.ValueContainer>);
        };
        var customOptionProject = function (projectProps) {
            var project = sentryProjectsById[projectProps.value];
            if (!project) {
                return null;
            }
            return (<components.Option {...projectProps}>
          <IdBadge project={project} avatarSize={20} displayName={project.slug} avatarProps={{ consistentWidth: true }}/>
        </components.Option>);
        };
        return (<Wrapper>
        {existingValues.map(renderItem)}
        <SelectContainer>
          <StyledSelectControl placeholder={t('Select a Project')} name="project" openMenuOnFocus options={projectOptions} components={{
            Option: customOptionProject,
            ValueContainer: customValueContainer,
        }} ref={this.sentryProjectRef}/>
          <StyledSelectControl placeholder={mappedDropdown.placeholder} name="mappedDropwdown" openMenuOnFocus options={mappedItemsToShow} ref={this.mappedRef}/>
          <Button size="small" label={t('Add')} icon={<IconAdd />} onClick={handleAdd}/>
        </SelectContainer>
      </Wrapper>);
    };
    return RenderField;
}(React.Component));
export { RenderField };
var ProjectMapperField = function (props) { return (<InputField {...props} field={function (renderProps) { return <RenderField {...renderProps}/>; }}/>); };
export default ProjectMapperField;
var StyledSelectControl = styled(SelectControl)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  width: 50%;\n"], ["\n  width: 50%;\n"])));
var SelectContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var Wrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject([""], [""])));
var Item = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  padding: 5px;\n"], ["\n  padding: 5px;\n"])));
var ItemValue = styled('span')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  padding: 5px;\n"], ["\n  padding: 5px;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=projectMapperField.jsx.map