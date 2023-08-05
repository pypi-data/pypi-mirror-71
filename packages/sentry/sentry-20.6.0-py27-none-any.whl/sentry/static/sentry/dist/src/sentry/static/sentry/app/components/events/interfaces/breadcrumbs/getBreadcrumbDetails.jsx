import React from 'react';
import HttpRenderer from 'app/components/events/interfaces/breadcrumbs/httpRenderer';
import ErrorRenderer from 'app/components/events/interfaces/breadcrumbs/errorRenderer';
import DefaultRenderer from 'app/components/events/interfaces/breadcrumbs/defaultRenderer';
import { IconInfo, IconLocation, IconRefresh, IconTerminal, IconUser, IconWarning, } from 'app/icons';
import { BreadcrumbType } from './types';
function getBreadcrumbDetails(breadcrumb) {
    switch (breadcrumb.type) {
        case BreadcrumbType.USER:
        case BreadcrumbType.UI: {
            return {
                color: 'purple',
                icon: <IconUser />,
                renderer: <DefaultRenderer breadcrumb={breadcrumb}/>,
            };
        }
        case BreadcrumbType.NAVIGATION: {
            return {
                color: 'blue400',
                icon: <IconLocation />,
                renderer: <DefaultRenderer breadcrumb={breadcrumb}/>,
            };
        }
        case BreadcrumbType.INFO: {
            return {
                color: 'blue400',
                icon: <IconInfo />,
                renderer: <DefaultRenderer breadcrumb={breadcrumb}/>,
            };
        }
        case BreadcrumbType.WARNING: {
            return {
                color: 'yellowOrange',
                borderColor: 'yellowOrangeDark',
                icon: <IconWarning />,
                renderer: <ErrorRenderer breadcrumb={breadcrumb}/>,
            };
        }
        case BreadcrumbType.EXCEPTION:
        case BreadcrumbType.MESSAGE:
        case BreadcrumbType.ERROR: {
            return {
                color: 'red',
                icon: <IconWarning />,
                renderer: <ErrorRenderer breadcrumb={breadcrumb}/>,
            };
        }
        case BreadcrumbType.HTTP: {
            return {
                color: 'green',
                icon: <IconRefresh />,
                renderer: <HttpRenderer breadcrumb={breadcrumb}/>,
            };
        }
        default:
            return {
                icon: <IconTerminal />,
                renderer: <DefaultRenderer breadcrumb={breadcrumb}/>,
            };
    }
}
export default getBreadcrumbDetails;
//# sourceMappingURL=getBreadcrumbDetails.jsx.map