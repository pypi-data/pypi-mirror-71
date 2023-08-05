import React from 'react';
import Feature from 'app/components/acl/feature';
import BreadcrumbsInterface from 'app/components/events/interfaces/breadcrumbs/breadcrumbs';
import Breadcrumbs from 'app/components/events/interfaces/breadcrumbsV2/breadcrumbs';
var EventEntriesBreadcrumbs = function (props) { return (<Feature features={['breadcrumbs-v2']}>
    {function (_a) {
    var hasFeature = _a.hasFeature;
    return hasFeature ? (<Breadcrumbs {...props}/>) : (<BreadcrumbsInterface {...props}/>);
}}
  </Feature>); };
export default EventEntriesBreadcrumbs;
//# sourceMappingURL=eventEntriesBreadcrumbs.jsx.map