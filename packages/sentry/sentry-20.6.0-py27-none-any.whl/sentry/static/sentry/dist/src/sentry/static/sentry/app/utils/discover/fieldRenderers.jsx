import { __makeTemplateObject } from "tslib";
import React from 'react';
import partial from 'lodash/partial';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import Count from 'app/components/count';
import Duration from 'app/components/duration';
import ProjectBadge from 'app/components/idBadge/projectBadge';
import UserBadge from 'app/components/idBadge/userBadge';
import UserMisery from 'app/components/userMisery';
import Version from 'app/components/version';
import getDynamicText from 'app/utils/getDynamicText';
import { formatFloat, formatPercentage } from 'app/utils/formatters';
import { getAggregateAlias, AGGREGATIONS } from 'app/utils/discover/fields';
import Projects from 'app/utils/projects';
import { BarContainer, Container, EventId, NumberContainer, OverflowLink, StyledDateTime, StyledShortId, VersionContainer, } from './styles';
var emptyValue = <span>{t('n/a')}</span>;
var EmptyValueContainer = styled(Container)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray500; });
/**
 * A mapping of field types to their rendering function.
 * This mapping is used when a field is not defined in SPECIAL_FIELDS
 * and the field is not being coerced to a link.
 *
 * This mapping should match the output sentry.utils.snuba:get_json_type
 */
var FIELD_FORMATTERS = {
    boolean: {
        isSortable: true,
        renderFunc: function (field, data) {
            var value = data[field] ? t('yes') : t('no');
            return <Container>{value}</Container>;
        },
    },
    date: {
        isSortable: true,
        renderFunc: function (field, data) { return (<Container>
        {data[field]
            ? getDynamicText({
                value: <StyledDateTime date={data[field]}/>,
                fixed: 'timestamp',
            })
            : emptyValue}
      </Container>); },
    },
    duration: {
        isSortable: true,
        renderFunc: function (field, data) { return (<NumberContainer>
        {typeof data[field] === 'number' ? (<Duration seconds={data[field] / 1000} fixedDigits={2} abbreviation/>) : (emptyValue)}
      </NumberContainer>); },
    },
    integer: {
        isSortable: true,
        renderFunc: function (field, data) { return (<NumberContainer>
        {typeof data[field] === 'number' ? <Count value={data[field]}/> : emptyValue}
      </NumberContainer>); },
    },
    number: {
        isSortable: true,
        renderFunc: function (field, data) { return (<NumberContainer>
        {typeof data[field] === 'number' ? formatFloat(data[field], 4) : emptyValue}
      </NumberContainer>); },
    },
    percentage: {
        isSortable: true,
        renderFunc: function (field, data) { return (<NumberContainer>
        {typeof data[field] === 'number' ? formatPercentage(data[field]) : emptyValue}
      </NumberContainer>); },
    },
    string: {
        isSortable: true,
        renderFunc: function (field, data) {
            // Some fields have long arrays in them, only show the tail of the data.
            var value = Array.isArray(data[field]) ? data[field].slice(-1) : data[field];
            return <Container>{value}</Container>;
        },
    },
};
/**
 * "Special fields" either do not map 1:1 to an single column in the event database,
 * or they require custom UI formatting that can't be handled by the datatype formatters.
 */
var SPECIAL_FIELDS = {
    id: {
        sortField: 'id',
        renderFunc: function (data) {
            var id = data === null || data === void 0 ? void 0 : data.id;
            if (typeof id !== 'string') {
                return null;
            }
            return (<Container>
          <EventId value={id}/>
        </Container>);
        },
    },
    'issue.id': {
        sortField: 'issue.id',
        renderFunc: function (data, _a) {
            var organization = _a.organization;
            var target = "/organizations/" + organization.slug + "/issues/" + data['issue.id'] + "/";
            return (<Container>
          <OverflowLink to={target} aria-label={data['issue.id']}>
            {data['issue.id']}
          </OverflowLink>
        </Container>);
        },
    },
    issue: {
        sortField: null,
        renderFunc: function (data, _a) {
            var organization = _a.organization;
            var issueID = data['issue.id'];
            if (!issueID) {
                return (<Container>
            <StyledShortId shortId={"" + data.issue}/>
          </Container>);
            }
            var target = "/organizations/" + organization.slug + "/issues/" + issueID + "/";
            return (<Container>
          <OverflowLink to={target} aria-label={issueID}>
            <StyledShortId shortId={"" + data.issue}/>
          </OverflowLink>
        </Container>);
        },
    },
    project: {
        sortField: 'project',
        renderFunc: function (data, _a) {
            var organization = _a.organization;
            return (<Container>
          <Projects orgId={organization.slug} slugs={[data.project]}>
            {function (_a) {
                var projects = _a.projects;
                var project = projects.find(function (p) { return p.slug === data.project; });
                return (<ProjectBadge project={project ? project : { slug: data.project }} avatarSize={16}/>);
            }}
          </Projects>
        </Container>);
        },
    },
    user: {
        sortField: 'user.id',
        renderFunc: function (data) {
            var userObj = {
                id: data.user,
                name: data.user,
                email: data.user,
                username: data.user,
                ip_address: '',
            };
            if (data.user) {
                var badge = <UserBadge user={userObj} hideEmail avatarSize={16}/>;
                return <Container>{badge}</Container>;
            }
            return <EmptyValueContainer>{emptyValue}</EmptyValueContainer>;
        },
    },
    release: {
        sortField: 'release',
        renderFunc: function (data) {
            return data.release && (<VersionContainer>
          <Version version={data.release} anchor={false} tooltipRawVersion truncate/>
        </VersionContainer>);
        },
    },
};
/**
 * "Special functions" are functions whose values either do not map 1:1 to a single column,
 * or they require custom UI formatting that can't be handled by the datatype formatters.
 */
var SPECIAL_FUNCTIONS = {
    user_misery: function (data) {
        var uniqueUsers = data.count_unique_user;
        var userMiseryField = '';
        for (var field in data) {
            if (field.startsWith('user_misery')) {
                userMiseryField = field;
            }
        }
        if (!userMiseryField) {
            return <NumberContainer>{emptyValue}</NumberContainer>;
        }
        var userMisery = data[userMiseryField];
        if (!uniqueUsers && uniqueUsers !== 0) {
            return (<NumberContainer>
          {typeof userMisery === 'number' ? formatFloat(userMisery, 4) : emptyValue}
        </NumberContainer>);
        }
        var miseryLimit = parseInt(userMiseryField.split('_').pop() || '', 10);
        return (<BarContainer>
        <UserMisery bars={10} barHeight={20} miseryLimit={miseryLimit} totalUsers={uniqueUsers} miserableUsers={userMisery}/>
      </BarContainer>);
    },
};
/**
 * Get the sort field name for a given field if it is special or fallback
 * to the generic type formatter.
 */
export function getSortField(field, tableMeta) {
    if (SPECIAL_FIELDS.hasOwnProperty(field)) {
        return SPECIAL_FIELDS[field].sortField;
    }
    if (!tableMeta) {
        return field;
    }
    for (var alias in AGGREGATIONS) {
        if (field.startsWith(alias)) {
            return AGGREGATIONS[alias].isSortable ? field : null;
        }
    }
    var fieldType = tableMeta[field];
    if (FIELD_FORMATTERS.hasOwnProperty(fieldType)) {
        return FIELD_FORMATTERS[fieldType].isSortable
            ? field
            : null;
    }
    return null;
}
/**
 * Get the field renderer for the named field and metadata
 *
 * @param {String} field name
 * @param {object} metadata mapping.
 * @returns {Function}
 */
export function getFieldRenderer(field, meta) {
    if (SPECIAL_FIELDS.hasOwnProperty(field)) {
        return SPECIAL_FIELDS[field].renderFunc;
    }
    var fieldName = getAggregateAlias(field);
    var fieldType = meta[fieldName];
    for (var alias in SPECIAL_FUNCTIONS) {
        if (fieldName.startsWith(alias)) {
            return SPECIAL_FUNCTIONS[alias];
        }
    }
    if (FIELD_FORMATTERS.hasOwnProperty(fieldType)) {
        return partial(FIELD_FORMATTERS[fieldType].renderFunc, fieldName);
    }
    return partial(FIELD_FORMATTERS.string.renderFunc, fieldName);
}
var templateObject_1;
//# sourceMappingURL=fieldRenderers.jsx.map