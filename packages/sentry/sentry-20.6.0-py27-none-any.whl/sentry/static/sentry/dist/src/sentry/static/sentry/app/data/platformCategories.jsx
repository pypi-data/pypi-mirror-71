import { __read, __spread } from "tslib";
import { t } from 'app/locale';
var popular = [
    'javascript',
    'javascript-react',
    'python-django',
    'python',
    'python-flask',
    'ruby-rails',
    'node-express',
    'php-laravel',
    'php-symfony2',
    'java',
    'csharp',
    'elixir',
    'php',
    'ruby',
    'node',
    'react-native',
    'javascript-angular',
];
var frontend = [
    'javascript',
    'javascript-react',
    'javascript-angular',
    'javascript-angularjs',
    'javascript-backbone',
    'javascript-ember',
    'javascript-vue',
];
var mobile = [
    'cocoa-objc',
    'cocoa-swift',
    'java-android',
    'cordova',
    'react-native',
];
var backend = [
    'csharp',
    'elixir',
    'go',
    'go-http',
    'java-appengine',
    'java',
    'java-log4j',
    'java-log4j2',
    'java-logback',
    'java-logging',
    'native',
    'node',
    'node-express',
    'node-koa',
    'node-connect',
    'php',
    'php-laravel',
    'php-monolog',
    'php-symfony2',
    'python',
    'python-django',
    'python-flask',
    'python-sanic',
    'python-celery',
    'python-bottle',
    'python-pylons',
    'python-pyramid',
    'python-tornado',
    'python-rq',
    'python-awslambda',
    'ruby',
    'ruby-rails',
    'ruby-rack',
    'rust',
];
var desktop = ['cocoa', 'csharp', 'java', 'electron', 'minidump', 'native'];
var categoryList = [
    { id: 'popular', name: t('Popular'), platforms: popular },
    { id: 'browser', name: t('Browser'), platforms: frontend },
    { id: 'server', name: t('Server'), platforms: backend },
    { id: 'mobile', name: t('Mobile'), platforms: mobile },
    { id: 'desktop', name: t('Desktop'), platforms: desktop },
];
export var sourceMaps = __spread(frontend, [
    'react-native',
    'cordova',
    'electron',
]);
export default categoryList;
//# sourceMappingURL=platformCategories.jsx.map