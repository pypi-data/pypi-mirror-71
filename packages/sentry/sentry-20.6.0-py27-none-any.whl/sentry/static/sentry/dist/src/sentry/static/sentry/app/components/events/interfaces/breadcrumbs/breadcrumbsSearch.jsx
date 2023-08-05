import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import TextField from 'app/components/forms/textField';
import { IconSearch, IconClose } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
var BreadCrumbsSearch = function (_a) {
    var searchTerm = _a.searchTerm, onChangeSearchTerm = _a.onChangeSearchTerm, onClearSearchTerm = _a.onClearSearchTerm;
    return (<Wrapper data-test-id="breadcumber-search">
    <StyledTextField name="breadcumber-search" placeholder={t('Search breadcrumbs...')} autoComplete="off" value={searchTerm} onChange={onChangeSearchTerm}/>
    <StyledIconSearch />
    <StyledIconClose show={!!searchTerm} onClick={onClearSearchTerm} isCircled/>
  </Wrapper>);
};
export default BreadCrumbsSearch;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n  display: flex;\n  align-items: center;\n"], ["\n  position: relative;\n  display: flex;\n  align-items: center;\n"])));
var StyledTextField = styled(TextField)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-bottom: 0;\n  input {\n    height: 28px;\n    padding-left: ", ";\n    padding-right: ", ";\n  }\n"], ["\n  margin-bottom: 0;\n  input {\n    height: 28px;\n    padding-left: ", ";\n    padding-right: ", ";\n  }\n"])), space(4), space(4));
var StyledIconSearch = styled(IconSearch)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  position: absolute;\n  color: ", ";\n  font-size: ", ";\n  left: ", ";\n"], ["\n  position: absolute;\n  color: ", ";\n  font-size: ", ";\n  left: ", ";\n"])), function (p) { return p.theme.gray500; }, function (p) { return p.theme.fontSizeMedium; }, space(1));
var StyledIconClose = styled(IconClose, {
    shouldForwardProp: function (p) { return p !== 'show'; },
})(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  position: absolute;\n  cursor: pointer;\n  color: ", ";\n  right: ", ";\n  visibility: ", ";\n"], ["\n  position: absolute;\n  cursor: pointer;\n  color: ", ";\n  right: ", ";\n  visibility: ", ";\n"])), function (p) { return p.theme.gray400; }, space(0.75), function (p) { return (p.show ? 'visible' : 'hidden'); });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=breadcrumbsSearch.jsx.map