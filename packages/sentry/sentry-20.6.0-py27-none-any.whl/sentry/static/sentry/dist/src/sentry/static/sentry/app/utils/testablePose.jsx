/* global process */
/**
 * Use with a react-pose animation to disable the animation in testing
 * environments.
 *
 * This function simply sets delays and durations to 0.
 */
var testablePose = !process.env.IS_PERCY
    ? function (a) { return a; }
    : function (animation) {
        Object.keys(animation).forEach(function (pose) {
            animation[pose].delay = 0;
            animation[pose].delayChildren = 0;
            animation[pose].staggerChildren = 0;
            animation[pose].transition = { duration: 0 };
        });
        return animation;
    };
export default testablePose;
//# sourceMappingURL=testablePose.jsx.map