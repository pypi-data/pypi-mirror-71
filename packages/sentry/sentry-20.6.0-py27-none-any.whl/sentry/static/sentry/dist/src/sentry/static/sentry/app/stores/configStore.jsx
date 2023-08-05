import moment from 'moment-timezone';
import Reflux from 'reflux';
import qs from 'query-string';
import { setLocale } from 'app/locale';
var configStoreConfig = {
    // When the app is booted we will _immediately_ hydrate the config store,
    // effecively ensureing this is not empty.
    config: {},
    init: function () {
        this.config = {};
    },
    get: function (key) {
        return this.config[key];
    },
    set: function (key, value) {
        var _a;
        this.config[key] = value;
        this.trigger((_a = {}, _a[key] = value, _a));
    },
    getConfig: function () {
        return this.config;
    },
    loadInitialData: function (config) {
        config.features = new Set(config.features || []);
        this.config = config;
        // Language code is passed from django
        var languageCode = config.languageCode;
        // TODO(dcramer): abstract this out of ConfigStore
        if (config.user) {
            config.user.permissions = new Set(config.user.permissions);
            moment.tz.setDefault(config.user.options.timezone);
            var queryString = {};
            // Parse query string for `lang`
            try {
                queryString = qs.parse(window.location.search) || {};
            }
            catch (err) {
                // ignore if this fails to parse
                // this can happen if we have an invalid query string
                // e.g. unencoded "%"
            }
            var queryStringLang = queryString.lang;
            if (Array.isArray(queryStringLang)) {
                queryStringLang = queryStringLang[0];
            }
            languageCode = queryStringLang || config.user.options.language || languageCode;
        }
        // Priority:
        // "?lang=en" --> user configuration options --> django request.LANGUAGE_CODE --> "en"
        setLocale(languageCode || 'en');
        this.trigger(config);
    },
};
export default Reflux.createStore(configStoreConfig);
//# sourceMappingURL=configStore.jsx.map