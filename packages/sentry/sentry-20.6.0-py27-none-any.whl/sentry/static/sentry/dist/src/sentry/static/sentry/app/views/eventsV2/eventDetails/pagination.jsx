import { __makeTemplateObject, __read } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import { IconPrevious, IconNext } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { eventDetailsRouteWithEventView } from 'app/utils/discover/urls';
/**
 * Generate a mapping of link names => link targets for pagination
 */
function buildTargets(event, eventView, organization) {
    var urlMap = {
        previous: event.previousEventID,
        next: event.nextEventID,
        oldest: event.oldestEventID,
        latest: event.latestEventID,
    };
    var links = {};
    Object.entries(urlMap).forEach(function (_a) {
        var _b = __read(_a, 2), key = _b[0], eventSlug = _b[1];
        // If the urlMap has no value we want to skip this link as it is 'disabled';
        if (!eventSlug) {
            links[key] = null;
        }
        else {
            links[key] = eventDetailsRouteWithEventView({
                eventSlug: eventSlug,
                eventView: eventView,
                orgSlug: organization.slug,
            });
        }
    });
    return links;
}
var Pagination = function (props) {
    var event = props.event, organization = props.organization, eventView = props.eventView;
    var links = buildTargets(event, eventView, organization);
    return (<Paginator merged>
      <Button size="small" to={links.oldest || ''} disabled={links.previous === null || links.oldest === null} icon={<IconPrevious size="xs"/>}/>
      <Button size="small" data-test-id="older-event" to={links.previous} disabled={links.previous === null}>
        {t('Older')}
      </Button>
      <Button size="small" data-test-id="newer-event" to={links.next} disabled={links.next === null}>
        {t('Newer')}
      </Button>
      <Button size="small" to={links.latest || ''} disabled={links.next === null || links.latest === null} icon={<IconNext size="xs"/>}/>
    </Paginator>);
};
var Paginator = styled(ButtonBar)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-top: ", ";\n\n  @media (min-width: ", ") {\n    margin-left: ", ";\n    margin-top: 0;\n  }\n"], ["\n  margin-top: ", ";\n\n  @media (min-width: ", ") {\n    margin-left: ", ";\n    margin-top: 0;\n  }\n"])), space(2), function (p) { return p.theme.breakpoints[1]; }, space(1.5));
export default Pagination;
var templateObject_1;
//# sourceMappingURL=pagination.jsx.map