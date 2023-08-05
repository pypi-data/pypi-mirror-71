import { t } from 'app/locale';
import slugify from 'app/utils/slugify';
// Export route to make these forms searchable by label/help
export var route = '/settings/:orgId/';
var formGroups = [
    {
        // Form "section"/"panel"
        title: t('General'),
        fields: [
            {
                name: 'slug',
                type: 'string',
                required: true,
                label: t('Name'),
                help: t('A unique ID used to identify this organization'),
                transformInput: slugify,
                saveOnBlur: false,
                saveMessageAlertType: 'info',
                saveMessage: t('You will be redirected to the new organization slug after saving'),
            },
            {
                name: 'name',
                type: 'string',
                required: true,
                label: t('Display Name'),
                help: t('This is the name that users will see for the organization'),
            },
            {
                name: 'isEarlyAdopter',
                type: 'boolean',
                label: t('Early Adopter'),
                help: t("Opt-in to new features before they're released to the public"),
            },
        ],
    },
    {
        title: 'Membership',
        fields: [
            {
                name: 'defaultRole',
                type: 'array',
                required: true,
                label: t('Default Role'),
                // seems weird to have choices in initial form data
                choices: function (_a) {
                    var initialData = (_a === void 0 ? {} : _a).initialData;
                    var _b, _c;
                    return (_c = (_b = initialData === null || initialData === void 0 ? void 0 : initialData.availableRoles) === null || _b === void 0 ? void 0 : _b.map(function (r) { return [r.id, r.name]; })) !== null && _c !== void 0 ? _c : [];
                },
                help: t('The default role new members will receive'),
                disabled: function (_a) {
                    var access = _a.access;
                    return !access.has('org:admin');
                },
            },
            {
                name: 'openMembership',
                type: 'boolean',
                required: true,
                label: t('Open Membership'),
                help: t('Allow organization members to freely join or leave any team'),
            },
            {
                name: 'eventsMemberAdmin',
                type: 'boolean',
                label: t('Grant Members Events Admin'),
                help: t('Allow members to delete events (including the delete & discard action) by granting them the `event:admin` scope.'),
            },
            {
                name: 'attachmentsRole',
                type: 'array',
                choices: function (_a) {
                    var _b = _a.initialData, initialData = _b === void 0 ? {} : _b;
                    var _c, _d;
                    return (_d = (_c = initialData === null || initialData === void 0 ? void 0 : initialData.availableRoles) === null || _c === void 0 ? void 0 : _c.map(function (r) { return [r.id, r.name]; })) !== null && _d !== void 0 ? _d : [];
                },
                label: t('Attachments Access'),
                help: t('Permissions required to download event attachments, such as native crash reports or log files.'),
                visible: function (_a) {
                    var features = _a.features;
                    return features.has('event-attachments');
                },
            },
        ],
    },
];
export default formGroups;
//# sourceMappingURL=organizationGeneralSettings.jsx.map