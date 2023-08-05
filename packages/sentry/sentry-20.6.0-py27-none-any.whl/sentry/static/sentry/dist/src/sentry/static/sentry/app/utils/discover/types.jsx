import { t } from 'app/locale';
export var DisplayModes;
(function (DisplayModes) {
    DisplayModes["DEFAULT"] = "default";
    DisplayModes["PREVIOUS"] = "previous";
    DisplayModes["RELEASES"] = "releases";
    DisplayModes["TOP5"] = "top5";
    DisplayModes["DAILY"] = "daily";
    DisplayModes["DAILYTOP5"] = "dailytop5";
})(DisplayModes || (DisplayModes = {}));
export var DISPLAY_MODE_OPTIONS = [
    { value: DisplayModes.DEFAULT, label: t('Total Period') },
    { value: DisplayModes.PREVIOUS, label: t('Previous Period') },
    { value: DisplayModes.RELEASES, label: t('Release Markers') },
    { value: DisplayModes.TOP5, label: t('Top 5 Period') },
    { value: DisplayModes.DAILY, label: t('Total Daily') },
    { value: DisplayModes.DAILYTOP5, label: t('Top 5 Daily') },
];
// default list of yAxis options
export var CHART_AXIS_OPTIONS = [
    { label: 'count()', value: 'count()' },
    { label: 'count_unique(users)', value: 'count_unique(user)' },
];
//# sourceMappingURL=types.jsx.map