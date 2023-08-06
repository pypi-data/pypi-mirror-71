define(["../Config/Index"], function(Config) {
    
    const PrintError = () => {
        if(Config.PROCESS_MODE === 1){
            // production MODE
            console.log("production");
        } else {
            // development MODE
            console.log("development");
            throw ""
        }
    }

    const AssertError = (errorString) => {
        throw errorString
    }

    const DispatchFrontEndError = () => {

    }

    return {
        PrintError,
        AssertError,
        DispatchFrontEndError
    }
});