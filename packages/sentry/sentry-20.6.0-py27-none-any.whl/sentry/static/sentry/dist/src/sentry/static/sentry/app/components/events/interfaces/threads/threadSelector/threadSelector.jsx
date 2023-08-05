import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import DropdownAutoComplete from 'app/components/dropdownAutoComplete';
import DropdownButton from 'app/components/dropdownButton';
import theme from 'app/utils/theme';
import { t } from 'app/locale';
import filterThreadInfo from './filterThreadInfo';
import getThreadException from './getThreadException';
import Option from './option';
import SelectedOption from './selectedOption';
import Header from './header';
var DROPDOWN_MAX_HEIGHT = 400;
var ThreadSelector = function (_a) {
    var threads = _a.threads, event = _a.event, activeThread = _a.activeThread, onChange = _a.onChange;
    var getDropDownItem = function (thread) {
        var threadInfo = filterThreadInfo(thread, event);
        var dropDownValue = "#" + thread.id + ": " + thread.name + " " + threadInfo.label + " " + threadInfo.filename;
        var crashedInfo;
        if (thread.crashed) {
            crashedInfo = getThreadException(thread, event);
        }
        return {
            value: dropDownValue,
            threadInfo: threadInfo,
            thread: thread,
            label: (<Option id={thread.id} details={threadInfo} name={thread.name} crashed={thread.crashed} crashedInfo={crashedInfo}/>),
        };
    };
    var handleOnChange = function (_a) {
        var thread = _a.thread;
        if (onChange) {
            onChange(thread);
        }
    };
    return (<StyledDropdownAutoComplete items={threads.map(getDropDownItem)} onSelect={handleOnChange} align="left" alignMenu="left" maxHeight={DROPDOWN_MAX_HEIGHT} placeholder={t('Filter Threads')} emptyMessage={t('You have no threads')} noResultsMessage={t('No threads found')} zIndex={theme.zIndex.dropdown} menuHeader={<Header />} closeOnSelect emptyHidesInput>
      {function (_a) {
        var isOpen = _a.isOpen, selectedItem = _a.selectedItem;
        return (<StyledDropdownButton size="small" isOpen={isOpen} align="left">
          {selectedItem ? (<SelectedOption id={selectedItem.thread.id} details={selectedItem.threadInfo}/>) : (<SelectedOption id={activeThread.id} details={filterThreadInfo(activeThread, event)}/>)}
        </StyledDropdownButton>);
    }}
    </StyledDropdownAutoComplete>);
};
export default ThreadSelector;
var StyledDropdownAutoComplete = styled(DropdownAutoComplete)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  width: 100%;\n  min-width: 300px;\n  @media (min-width: ", ") {\n    width: 500px;\n  }\n  @media (max-width: ", ") {\n    top: calc(100% - 2px);\n  }\n"], ["\n  width: 100%;\n  min-width: 300px;\n  @media (min-width: ", ") {\n    width: 500px;\n  }\n  @media (max-width: ", ") {\n    top: calc(100% - 2px);\n  }\n"])), theme.breakpoints[0], function (p) { return p.theme.breakpoints[2]; });
var StyledDropdownButton = styled(DropdownButton)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  > *:first-child {\n    grid-template-columns: 1fr 15px;\n  }\n  width: 100%;\n  min-width: 150px;\n  @media (min-width: ", ") {\n    max-width: 420px;\n  }\n"], ["\n  > *:first-child {\n    grid-template-columns: 1fr 15px;\n  }\n  width: 100%;\n  min-width: 150px;\n  @media (min-width: ", ") {\n    max-width: 420px;\n  }\n"])), function (props) { return props.theme.breakpoints[3]; });
var templateObject_1, templateObject_2;
//# sourceMappingURL=threadSelector.jsx.map