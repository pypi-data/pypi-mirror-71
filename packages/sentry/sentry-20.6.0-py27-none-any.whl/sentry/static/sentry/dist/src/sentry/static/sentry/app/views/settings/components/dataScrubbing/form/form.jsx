import { __assign, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import sortBy from 'lodash/sortBy';
import space from 'app/styles/space';
import { t } from 'app/locale';
import TextField from 'app/components/forms/textField';
import EventIdField from './eventIdField';
import FormField from './formField';
import SelectField from './selectField';
import SourceField from './sourceField';
import { getRuleLabel, getMethodLabel } from '../utils';
import { MethodType, RuleType, } from '../types';
var Form = function (_a) {
    var rule = _a.rule, errors = _a.errors, sourceSuggestions = _a.sourceSuggestions, onUpdateEventId = _a.onUpdateEventId, eventId = _a.eventId, onChange = _a.onChange, onValidate = _a.onValidate;
    var source = rule.source, type = rule.type, method = rule.method;
    return (<Wrapper>
      <GroupField hasTwoColumns={rule.method === MethodType.REPLACE}>
        <FormField label={t('Method')} tooltipInfo={t('What to do')}>
          <SelectField placeholder={t('Select method')} name="method" options={sortBy(Object.values(MethodType)).map(function (value) { return (__assign(__assign({}, getMethodLabel(value)), { value: value })); })} value={method} onChange={function (_a) {
        var value = _a.value;
        return onChange('method', value);
    }}/>
        </FormField>
        {rule.method === MethodType.REPLACE && (<FormField label={t('Custom Placeholder (Optional)')} tooltipInfo={t('It will replace the default placeholder [Filtered]')}>
            <StyledTextField name="placeholder" placeholder={"[" + t('Filtered') + "]"} onChange={function (value) {
        onChange('placeholder', value);
    }} value={rule.placeholder}/>
          </FormField>)}
      </GroupField>
      <GroupField hasTwoColumns={rule.type === RuleType.PATTERN}>
        <FormField label={t('Data Type')} tooltipInfo={t('What to look for. Use an existing pattern or define your own using regular expressions.')}>
          <SelectField placeholder={t('Select type')} name="type" options={sortBy(Object.values(RuleType)).map(function (value) { return ({
        label: getRuleLabel(value),
        value: value,
    }); })} value={type} onChange={function (_a) {
        var value = _a.value;
        return onChange('type', value);
    }}/>
        </FormField>
        {rule.type === RuleType.PATTERN && (<FormField label={t('Regex matches')} tooltipInfo={t('Custom Perl-style regex (PCRE)')}>
            <RegularExpression name="pattern" placeholder={t('[a-zA-Z0-9]+')} onChange={function (value) {
        onChange('pattern', value);
    }} value={rule.pattern} onBlur={onValidate('pattern')} error={errors === null || errors === void 0 ? void 0 : errors.pattern}/>
          </FormField>)}
      </GroupField>
      {onUpdateEventId && (<EventIdField onUpdateEventId={onUpdateEventId} eventId={eventId}/>)}
      <FormField label={t('Source')} tooltipInfo={t('Where to look. In the simplest case this can be an attribute name.')}>
        <SourceField onChange={function (value) {
        onChange('source', value);
    }} value={source} onBlur={onValidate('source')} isRegExMatchesSelected={type === RuleType.PATTERN} suggestions={sourceSuggestions} error={errors === null || errors === void 0 ? void 0 : errors.source}/>
      </FormField>
    </Wrapper>);
};
export default Form;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-row-gap: ", ";\n"], ["\n  display: grid;\n  grid-row-gap: ", ";\n"])), space(2));
var GroupField = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  @media (min-width: ", ") {\n    ", "\n  }\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  @media (min-width: ", ") {\n    ", "\n  }\n"])), space(2), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.hasTwoColumns && "grid-template-columns: 1fr 1fr;"; });
var StyledTextField = styled(TextField)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  height: 40px;\n  input {\n    height: 40px;\n  }\n  ", "\n  @media (min-width: ", ") {\n    margin-bottom: 0;\n  }\n"], ["\n  height: 40px;\n  input {\n    height: 40px;\n  }\n  ", "\n  @media (min-width: ", ") {\n    margin-bottom: 0;\n  }\n"])), function (p) { return !p.error && "margin-bottom: 0;"; }, function (p) { return p.theme.breakpoints[0]; });
var RegularExpression = styled(StyledTextField)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-size: ", ";\n  input {\n    font-family: ", ";\n  }\n"], ["\n  font-size: ", ";\n  input {\n    font-family: ", ";\n  }\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.text.familyMono; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=form.jsx.map