define([], function() {

    const MakeDummyNumberArray = (const_lengthNumber) => {
        return Array.from({ const_lengthNumber }, (_, i) => 0 + i);
    };

    const MakeDummyNumberArray_AtoB = (const_lengthNumber) => {
        return Array.from({ const_lengthNumber }, (_, i) => 0 + i);
    };

    const MapOneArrayToDoubleArray = ( ref_oneDimensionArray, 
                                       const_showDataCountNumber, 
                                       const_columnNumber ) => {
        const return_doubleArray = [];
        let temp_innerArray = [];

        for (let i = 0; i < const_showDataCountNumber; i++){
            if (i !== 0 && i % const_columnNumber === 0){
                return_doubleArray.push(temp_innerArray);
                temp_innerArray = [];
            }
            temp_innerArray.push(ref_oneDimensionArray[i]);
        }
        
        return_doubleArray.push(temp_innerArray);

        return return_doubleArray;
    };

    return {
        MakeDummyNumberArray,
        MakeDummyNumberArray_AtoB,
        MapOneArrayToDoubleArray
    }
});