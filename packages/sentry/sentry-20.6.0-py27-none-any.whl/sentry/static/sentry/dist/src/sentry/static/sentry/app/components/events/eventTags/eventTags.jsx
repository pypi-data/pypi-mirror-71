import { __makeTemplateObject } from "tslib";
import React from 'react';
import isEmpty from 'lodash/isEmpty';
import styled from '@emotion/styled';
import EventDataSection from 'app/components/events/eventDataSection';
import { generateQueryWithTag } from 'app/utils';
import { t } from 'app/locale';
import Pills from 'app/components/pills';
import { getMeta } from 'app/components/events/meta/metaProxy';
import space from 'app/styles/space';
import EventTagsPill from './eventTagsPill';
var EventTags = function (_a) {
    var tags = _a.event.tags, orgId = _a.orgId, projectId = _a.projectId, location = _a.location;
    if (isEmpty(tags)) {
        return null;
    }
    var streamPath = "/organizations/" + orgId + "/issues/";
    var releasesPath = "/organizations/" + orgId + "/releases/";
    return (<StyledEventDataSection title={t('Tags')} type="tags">
      <Pills>
        {tags.map(function (tag) { return (<EventTagsPill key={tag.key} tag={tag} projectId={projectId} orgId={orgId} query={generateQueryWithTag(location.query, tag)} streamPath={streamPath} releasesPath={releasesPath} meta={getMeta(tag, 'value')}/>); })}
      </Pills>
    </StyledEventDataSection>);
};
export default EventTags;
var StyledEventDataSection = styled(EventDataSection)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  @media (min-width: ", ") {\n    margin-bottom: ", ";\n  }\n"], ["\n  @media (min-width: ", ") {\n    margin-bottom: ", ";\n  }\n"])), function (p) { return p.theme.breakpoints[1]; }, space(3));
var templateObject_1;
//# sourceMappingURL=eventTags.jsx.map