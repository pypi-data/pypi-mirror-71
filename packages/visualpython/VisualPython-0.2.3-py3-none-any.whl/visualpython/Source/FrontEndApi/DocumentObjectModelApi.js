
define([], function() {

    const GetDom = (const_tagName) => { 
        return document.querySelector(const_tagName);
    }

    const GetDomList = (const_tagName) => { 
        return document.querySelectorAll(const_tagName);
    }
    /*
        @param1 const_tagName <String>
        @param2 attribute <Object> -optional-

        @return return_dom <Document>
    */
   
    const MakeDom = (const_tagName, attribute = {}) => {
        const return_dom = Object.entries(attribute).reduce((element, value) => {
            typeof element[value[0]] === 'function' 
                            ? element[value[0]](value[1]) 
                            : (element[value[0]] = value[1]);
            return element;
        }, document.createElement(const_tagName));

        return return_dom;
    }

    /*
        MakeDom함수 예제
        MakeDom("div", { onclick:function(event) {console.log(1);} ,
                         innerHTML:"안녕하세요",
                         classList:"white"  });
            -> <div class=​"white">​안녕하세요</div>​

        MakeDom("div", { onclick: function(event) {
                                    console.log(1);
                                } 
                       }
                );
            -> <div></div>​
            
        MakeDom("div", { 
                        onclick: async () => {
                                  const a = await Math.random();
                                  console.log("a",a);
                                 },
                        innerHTML:"cccccccc" 
                        }
                );

        MakeDom("div", { classList:"white" });
            -> <div class=​"white">​</div>​

        MakeDom("div", { innerHTML:"안녕하세요"});
            -> <div>​안녕하세요</div>​
        
        MakeDom("div", { classList:"white",
                        innerHTML:"안녕하세요" });
            -> <div class=​"white">안녕하세요​</div>​
    */

    return {
        GetDom,
        GetDomList,

        MakeDom
    }
});