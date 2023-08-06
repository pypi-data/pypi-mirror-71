define([], function() {

    const CheckIsInstance = (childClass, parentClass) => {
        return childClass instanceof parentClass
    };

    return {
        CheckIsInstance
    }
});