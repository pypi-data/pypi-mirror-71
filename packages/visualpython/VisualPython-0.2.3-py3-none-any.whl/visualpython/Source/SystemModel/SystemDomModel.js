define([
    "base/js/namespace",

    "nbextensions/visualpython/Source/Config/Index",
    "nbextensions/visualpython/Source/FrontEndApi/Index"
], function(
    Jupyter,

    Config,
    FrontEndApis) {

    const AWS_S3_CSVDATA_URL = Config.AWS_S3_CSVDATA_URL;

    const DocumentObjectModelApi = FrontEndApis.DocumentObjectModelApi;
    const JupyterNativeApi = FrontEndApis.JupyterNativeApi;

    const SystemDomModel = class {

        static m_MainDom = null;
        static m_MainDomBody = null;
        static m_IsShowMainDom = true;

        static m_TemplateDomButtonArr = [];
        static m_MainNavTabDomArr = [];

        constructor(){

        }

        static InitializeSystemDom = () => {
            // 메인 
            this.m_MainDom = $(".MainContainer-container");
            this.m_MainDomBody = $(".MainContainer-bottom-body");

            // 메인 페이지 들
            const dom_templatePage = $(`<div class="TemplatePage-container">
                    <div class="TemplatePage-inner-title color-DC6180">
                        Template
                    </div>
                    <div class="TemplatePage-inner-body">
                        <div class="TemplatePage-inner-container scrollbar">

                            <div class="TemplatePage-block">
                                <div class="TemplatePage-block-title">
                                    표준 라이브러리 호출
                                </div>
                                <div class="TemplatePage-block-body">
                                    <input id="import-standard-library" class="Base-input-button" type="submit" value="Import 기본" />
                                    <input id="import-standard-library-2" class="Base-input-button" type="submit" value="케라스" />
                                    <input id="import-standard-library-3" class="Base-input-button" type="submit" value="텐서플로우" />
                                </div>
                            </div>

                            <div class="TemplatePage-block">
                                <div class="TemplatePage-block-title">
                                    CSV
                                </div>
                                <div class="TemplatePage-block-body">
                                    <input id="btn-import-samplecsv-test" class="Base-input-button " type="submit" value="테스트 csv" />
                                    <input id="btn-import-samplecsv-welfareCenter" class="Base-input-button" type="submit" value="복지관 csv" />
                                    <input id="btn-import-samplecsv-stockprice" class="Base-input-button" type="submit" value="주식 csv" />
                                </div>
                            </div>

                            <div class="TemplatePage-block">
                                <div class="TemplatePage-block-title">
                                    판다스
                                </div>
                                <div class="TemplatePage-block-body">
                                    <input id="btn-pandas-1" class="Base-input-button" type="submit" value="판다스 1" />
                                    <input id="btn-pandas-2" class="Base-input-button" type="submit" value="판다스 2" />
                                    <input id="btn-pandas-3" class="Base-input-button" type="submit" value="판다스 3" />
                                </div>
                            </div>

                            <div class="TemplatePage-block">
                                <div class="TemplatePage-block-title">
                                    넘파이
                                </div>
                                <div class="TemplatePage-block-body">
                                    <input id="btn-numpy-1" class="Base-input-button" type="submit" value="넘파이 1" />
                                    <input id="btn-numpy-2" class="Base-input-button" type="submit" value="넘파이 2" />
                                    <input id="btn-numpy-3" class="Base-input-button" type="submit" value="넘파이 3" />
                                </div>
                            </div>

                            <div class="TemplatePage-block">
                                <div class="TemplatePage-block-title">
                                    머신러닝 기본
                                </div>
                                <div class="TemplatePage-block-body">
                                    <input id="btn-basic-ml-1" class="Base-input-button" type="submit" value="ML Basic 1" />
                                    <input id="btn-basic-ml-2" class="Base-input-button" type="submit" value="ML Basic 2" />
                                    <input id="btn-basic-ml-3" class="Base-input-button" type="submit" value="ML Basic 3" />
                                </div>
                            </div>

                            <div class="TemplatePage-block">
                                <div class="TemplatePage-block-title">
                                    머신러닝 응용
                                </div>
                                <div class="TemplatePage-block-body">
                                    <input id="btn-ml-1" class="Base-input-button" type="submit" value="머신러닝 1" />
                                    <input id="btn-ml-2" class="Base-input-button" type="submit" value="머신러닝 2" />
                                    <input id="btn-ml-3" class="Base-input-button" type="submit" value="머신러닝 3" />
                                </div>
                            </div>

                            <div class="TemplatePage-block">
                                <div class="TemplatePage-block-title">
                                    네이버 최신 기사 크롤링
                                </div>
                                <div class="TemplatePage-block-body">
                                    <input id="search-naver-crawling" class="Base-input-search" type="text"/>
                                    <div class="TemplatePage-block-body-button-container">
                                        <input id="btn-naver-crawling" class="Base-input-button" type="submit" value="검색" />
                                    </div>
                                </div>
                            </div>

                        </div>
                    </div>
                </div>`);

            dom_templatePage.appendTo('.MainContainer-bottom-body');

            const dom_loginPage = $(`<div class="LoginPage-container">

                <div class="LoginPage-title">
                    <p class="LoginPage-title-text color-DC6180">Login to your account</p>
                </div>

                <div class="LoginPage-body">
                    <div class="LoginPage-body-element-container">

                        <div class="LoginPage-body-element">
                            <div class="LoginPage-body-element-icon">
                                <img src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/user_icon_copy.png"/>
                            </div>
                            <input class="LoginPage-body-element-input-id" placeholder="아이디" type="text" />
                        </div>

                        <div class="LoginPage-body-element">
                            <div class="LoginPage-body-element-icon">
                                <img src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/217233/lock_icon_copy.png"/>
                            </div>
                            <input class="LoginPage-body-element-input-password" placeholder="패스워드" type="password" />
                        </div>
                    </div>

                    <div class="LoginPage-body-submit">
                        <input class="LoginPage-body-submit-input-login" type="submit" value="Log In" />

                        <input class="LoginPage-body-submit-input-signup" type="submit" value="Sign Up" />
                    </div>

                    <div class="LoginPage-body-a-forgetPassword">
                        <a href="#">
                            비밀번호를 잊어버리셨나요?
                        </a>
                    </div>
                </div>
            </div>`);

            const dom_codeEditorPage = $(`<div class="CodeEditorPage-container">
                <div class="CodeEditorPage-inner-title color-DC6180">
                    Code Editor
                </div>
                <div class="CodeEditorPage-inner-body">
                    <div class="CodeEditorPage-inner-container scrollbar">
                        <div class="CodeEditorPage-codeBlock">
                            <div class="CodeEditorPage-codeBlock-title">
                                [1]
                            </div>
                            <div class="CodeEditorPage-codeBlock-body">
                                <textarea>
        
                                </textarea>
                            </div>
                            <div class="CodeEditorPage-codeBlock-toolbar">
                                <input class="CodeEditorPage-codeBlock-input-button visual-python-cell-execute-button" type="submit" value="비주얼 파이썬 셀 실행" />
                                <input class="CodeEditorPage-codeBlock-input-button visual-python-cell-reset-button" type="submit" value="비주얼 파이썬 셀 초기화" />
                                <input class="CodeEditorPage-codeBlock-input-button jupyter-cell-get-button" type="submit" value="주피터 셀 가져오기" />
                                <input class="CodeEditorPage-codeBlock-input-button jupyter-cell-reset-button" type="submit" value="주피터 셀 초기화" />
                                <input class="CodeEditorPage-codeBlock-input-button codeEditor-option-button" type="submit" value="옵션" />
                            </div>
                        </div>
        
                        <div class="CodeEditorPage-codeBlock">
                            <div class="CodeEditorPage-codeBlock-title">
                                [2]
                            </div>
                            <div class="CodeEditorPage-codeBlock-body">
                                <textarea>
                                    
                                </textarea>
                            </div>
                            <div class="CodeEditorPage-codeBlock-toolbar">
                                <input class="CodeEditorPage-codeBlock-input-button visual-python-cell-execute-button" type="submit" value="비주얼 파이썬 셀 실행" />
                                <input class="CodeEditorPage-codeBlock-input-button visual-python-cell-reset-button" type="submit" value="비주얼 파이썬 셀 초기화" />
                                <input class="CodeEditorPage-codeBlock-input-button jupyter-cell-get-button" type="submit" value="주피터 셀 가져오기" />
                                <input class="CodeEditorPage-codeBlock-input-button jupyter-cell-reset-button" type="submit" value="주피터 셀 초기화" />
                                <input class="CodeEditorPage-codeBlock-input-button codeEditor-option-button" type="submit" value="옵션" />
                            </div>
                        </div>
        
                        <div class="CodeEditorPage-codeBlock">
                            <div class="CodeEditorPage-codeBlock-title">
                                [3]
                            </div>
                            <div class="CodeEditorPage-codeBlock-body">
                                <textarea>
                                    
                                </textarea>
                            </div>
                            <div class="CodeEditorPage-codeBlock-toolbar">
                                <input class="CodeEditorPage-codeBlock-input-button visual-python-cell-execute-button" type="submit" value="비주얼 파이썬 셀 실행" />
                                <input class="CodeEditorPage-codeBlock-input-button visual-python-cell-reset-button" type="submit" value="비주얼 파이썬 셀 초기화" />
                                <input class="CodeEditorPage-codeBlock-input-button jupyter-cell-get-button" type="submit" value="주피터 셀 가져오기" />
                                <input class="CodeEditorPage-codeBlock-input-button jupyter-cell-reset-button" type="submit" value="주피터 셀 초기화" />
                                <input class="CodeEditorPage-codeBlock-input-button codeEditor-option-button" type="submit" value="옵션" />
                            </div>
                        </div>
                    </div>
                </div>
            </div>`);
            
            const dom_li_codeEditor = DocumentObjectModelApi.GetDom(".MainContainer-li-codeEditor");
            const dom_li_template = DocumentObjectModelApi.GetDom(".MainContainer-li-template");
            const dom_li_login = DocumentObjectModelApi.GetDom(".MainContainer-li-login");
            const dom_li_signUp = DocumentObjectModelApi.GetDom(".MainContainer-li-signUp");
            const dom_li_setting = DocumentObjectModelApi.GetDom(".MainContainer-li-setting");

            dom_li_codeEditor.addEventListener('click', () => {
                this.m_MainDomBody.empty();
                dom_codeEditorPage.appendTo(this.m_MainDomBody);
            });
            dom_li_template.addEventListener('click', () => {
                this.m_MainDomBody.empty();
                dom_templatePage.appendTo(this.m_MainDomBody);
            });
            dom_li_login.addEventListener('click', () => {
                this.m_MainDomBody.empty();
                dom_loginPage.appendTo(this.m_MainDomBody);
            });
            dom_li_signUp.addEventListener('click', () => {
                
            });
            dom_li_setting.addEventListener('click', () => {
                
            });

            // import 표준 라이브러리
            const btn_importStandardLibrary = DocumentObjectModelApi.GetDom("#import-standard-library");
            btn_importStandardLibrary.addEventListener('click', () => {
                const str = `# Import Standard libraries\nimport pandas as pd\nimport numpy as np\n\n`;

                const str2 = `from sklearn import datasets, linear_model\n`;
                const str3 = `from sklearn.metrics import mean_squared_error, r2_score\n`;

                const str4 = `from sklearn.pipeline import make_pipeline\n`;
                const str5 = `from sklearn.preprocessing import StandardScaler\n`;
                const str6 = `from sklearn.neighbors import KNeighborsClassifier\n\n`;
               
                const str7 = `import matplotlib.pyplot as plt\n`;

                const importStandardLibraryStr = str + str2 + str3 + str4 + str5 + str6 + str7;
                JupyterNativeApi.SetCodeAndExecute(importStandardLibraryStr);

            });
            this.m_TemplateDomButtonArr.push({
                name: "btn_importStandardLibrary",
                dom: btn_importStandardLibrary
            });

            // import sample test csv data
            const btn_importSampleTestCsv = DocumentObjectModelApi.GetDom("#btn-import-samplecsv-test");
            btn_importSampleTestCsv.addEventListener('click', () => {
                const str = `test_data = pd.read_csv("${AWS_S3_CSVDATA_URL}/test_csv_file.csv")\ntest_data`;
                JupyterNativeApi.SetCodeAndExecute(str);
            });
            this.m_TemplateDomButtonArr.push({
                name: "btn_importSampleTestCsv",
                dom: btn_importSampleTestCsv
            });

            // import sample welfareCenter csv data
            const btn_importSampleWelfareCenterCsv = DocumentObjectModelApi.GetDom("#btn-import-samplecsv-welfareCenter");
            btn_importSampleWelfareCenterCsv.addEventListener('click', () => {
                const str = `welfareCenter_data = pd.read_csv("${AWS_S3_CSVDATA_URL}/welfareCenter.csv")\nwelfareCenter_data`;
                JupyterNativeApi.SetCodeAndExecute(str);
            });
            this.m_TemplateDomButtonArr.push({
                name: "btn_importSampleWelfareCenterCsv",
                dom: btn_importSampleWelfareCenterCsv
            });

            // import sample stockptice csv data
            const btn_importSampleStockPriceCsv = DocumentObjectModelApi.GetDom("#btn-import-samplecsv-stockprice");
            btn_importSampleStockPriceCsv.addEventListener('click', () => {
                const str = `stockPrice_data = pd.read_csv("${AWS_S3_CSVDATA_URL}/stockPrice.csv", error_bad_lines=False)\nstockPrice_data`;
                JupyterNativeApi.SetCodeAndExecute(str);
            });
            this.m_TemplateDomButtonArr.push({
                name: "btn_importSampleStockPriceCsv",
                dom: btn_importSampleStockPriceCsv
            });

            // 판다스 1
            const btn_pandas1 = DocumentObjectModelApi.GetDom("#btn-pandas-1");
            btn_pandas1.addEventListener('click', () => {
                const str = `data_A = {'key': [1,2,3], 'name': ['Jane', 'John', 'Peter']}\ndataframe_A = pd.DataFrame(data_A, columns = ['key', 'name'])`;
                JupyterNativeApi.SetCodeAndExecute(str);

                const str2 = `data_B = {'key': [2,3,4], 'age': [18, 15, 20]}\ndataframe_B = pd.DataFrame(data_B, columns = ['key', 'age'])`;
                JupyterNativeApi.SetCodeAndExecute(str2);

                const str3 = `print(dataframe_A)\nprint(dataframe_B)`;
                JupyterNativeApi.SetCodeAndExecute(str3);

                const str4 = `df_INNER_JOIN = pd.merge(dataframe_A, dataframe_B, left_on='key', right_on='key', how='inner')\nprint(df_INNER_JOIN)`;
                JupyterNativeApi.SetCodeAndExecute(str4);
                
                const str5 = `df_OUTER_JOIN = pd.merge(dataframe_A, dataframe_B, left_on='key', right_on='key', how='outer')\nprint(df_OUTER_JOIN)`;
                JupyterNativeApi.SetCodeAndExecute(str5);

                const str6 = `df_LEFT_JOIN = pd.merge(dataframe_A, dataframe_B, left_on='key', right_on='key', how='left')\nprint(df_LEFT_JOIN)`;
                JupyterNativeApi.SetCodeAndExecute(str6);

                const str7 = `df_RIGHT_JOIN = pd.merge(dataframe_A, dataframe_B, left_on='key', right_on='key', how='right')\nprint(df_RIGHT_JOIN)`;
                JupyterNativeApi.SetCodeAndExecute(str7);
            });
            this.m_TemplateDomButtonArr.push({
                name: "btn_pandas1",
                dom: btn_pandas1
            });

            const btn_basic_ml_1 = DocumentObjectModelApi.GetDom("#btn-basic-ml-1"); 
            btn_basic_ml_1.addEventListener('click', () => {
                const str1 = `def AND(x1,x2):\n`;
                const str2 = `  w1, w2, b = 0.5, 0.5, 0.7\n`;
                const str3 = `  tmp = w1*x1 + w2*x2\n`;
                const str4 = `  if tmp <= b:\n`;
                const str5 = `    return 0\n`;
                const str6 = `  else:\n`;
                const str7 = `    return 1\n`;
                const str8 = `AND(0, 0)\n\n`;

                const andFuncStr = str1 + str2 + str3 + str4 + str5 + str6 + str7 + str8;
                JupyterNativeApi.SetCodeAndExecute(andFuncStr);

                const str2_1 = `def NAND(x1,x2):\n`;
                const str2_2 = `  w1, w2, b = -0.5, -0.5, -0.7\n`;
                const str2_3 = `  tmp = w1*x1 + w2*x2\n`;
                const str2_4 = `  if tmp <= b:\n`;
                const str2_5 = `    return 0\n`;
                const str2_6 = `  else:\n`;
                const str2_7 = `    return 1\n`;
                const str2_8 = `NAND(1, 1)\n\n`;

                const nandFuncStr = str2_1 + str2_2 + str2_3 + str2_4 + str2_5 + str2_6 + str2_7 + str2_8;
                JupyterNativeApi.SetCodeAndExecute(nandFuncStr);

                const str3_1 = `def OR(x1,x2):\n`;
                const str3_2 = `    w1, w2, b = -0.5, 0.5, 0\n`;
                const str3_3 = `    tmp = w1*x1 + w2*x2\n`;
                const str3_4 = `    if tmp <= b:\n`;
                const str3_5 = `      return 0\n`;
                const str3_6 = `    else:\n`;
                const str3_7 = `      return 1\n`;
                const str3_8 = `OR(0, 1)\n\n`;

                const orFuncStr = str3_1 + str3_2 + str3_3 + str3_4 + str3_5 + str3_6 + str3_7 + str3_8;
                JupyterNativeApi.SetCodeAndExecute(orFuncStr);

                const str4_1 = `def XOR(x1,x2):\n`;
                const str4_2 = `    s1 = NAND(x1, x2)\n`;
                const str4_3 = `    s2 = OR(x1, x2)\n`;
                const str4_4 = `    y = AND(s1, s2)\n`;
                const str4_5 = `    return y\n\n`;
                const str4_6 = `XOR(1, 1)\n\n`;

                const xorFuncStr = str4_1 + str4_2 + str4_3 + str4_4 + str4_5 + str4_6;
                JupyterNativeApi.SetCodeAndExecute(xorFuncStr);

                const str5_1 = `def softmax(x):\n`;
                const str5_2 = `    e_x = np.exp(x - np.max(x))\n`;
                const str5_3 = `    return e_x / e_x.sum()\n\n`;
                const str5_4 = `x = np.array([2.0,3.0,4.0,5.0,6.0])\n`;
                const str5_5 = `y = softmax(x)\n`;
                const str5_6 = `print(np.sum(y))\n`;
                const str5_7 = `ratio = y\n`;
                const str5_8 = `labels = y\n`;
                const str5_9 = `plt.pie(ratio, labels=labels, shadow=True, startangle=90)\n`;
                const str5_10 = `plt.show()\n`;

                const softmaxFuncStr = str5_1 + str5_2 + str5_3 + str5_4 + str5_5 + str5_6 + str5_7 + str5_8 + str5_9 + str5_10 ;
                JupyterNativeApi.SetCodeAndExecute(softmaxFuncStr);

            });

            const btn_basic_ml_2 = DocumentObjectModelApi.GetDom("#btn-basic-ml-2"); 
            btn_basic_ml_2.addEventListener('click', () => {
                const str1 = `# 선형회귀\n`;
                const str2 = `# 일하는 시간에 따른 일당에 대한 데이터는 아래와 같다.\n`;
                const str3 = `# 1 25,000\n`;
                const str4 = `# 2 55,000\n`;
                const str5 = `# 3 75,000\n`;
                const str6 = `# 4 110,000\n`;
                const str7 = `# 5 128,000\n`;
                const str8 = `# 6 155,000\n`;
                const str9 = `# 7 180,000\n`;
                const str10 = `# 10시간일 때 일당을 예측하시오\n\n`;
                
                const str11 = `import tensorflow as tf\n\n`;
                const str12 = `xData = [10,2,3,4,5]\n`;
                const str13 = `yData = [120, 130, 145, 157, 169]\n\n`;
                const str14 = `W = tf.Variable(tf.random_uniform ([1], -100, 100))\n`;
                const str15 = `b = tf.Variable(tf.random_uniform ([1], -100, 100))\n\n`;
                const str16 = `x = tf.placeholder(tf.float32)\n`;
                const str17 = `y = tf.placeholder(tf.float32)\n`;
                const str18 = `H = W * x + b\n`;
                const str19 = `cost = tf.reduce_mean(tf.square (H-y))\n`;
                const str20 = `a = tf.Variable(0.01)\n\n`;

                const str21 = `optimizer = tf.train.GradientDescentOptimizer(a)\n`;
                const str22 = `train = optimizer.minimize(cost)\n`;
                const str23 = `init = tf.global_variables_initializer()\n`;
                const str24 = `sess = tf.Session()\n`;
                const str25 = `sess.run(init)\n\n`;

                const str26 = `for i in range(5001):\n`;
                const str27 = `    sess.run(train, feed_dict={x: xData, y: yData})\n`;
                const str28 = `    if i % 50 == 0:\n`;
                const str29 = `        print(i, sess.run(cost, feed_dict={x: xData, y: yData}), sess.run(W), sess.run(b))\n`;

                const linearRegressionStr = str1 + str2 + str3 + str4 + str5 + str6 + str7 + str8 + str9 + str10 +
                                            str11 + str12 + str13 + str14 + str15 + str16 + str17 + str18 + str19 + str20 +
                                            str21 + str22 + str23 + str24 + str25 + str26 + str27 + str28 + str29;
                JupyterNativeApi.SetCodeAndExecute(linearRegressionStr);
            });

            const btn_basic_ml_3 = DocumentObjectModelApi.GetDom("#btn-basic-ml-3"); 
            btn_basic_ml_3.addEventListener('click', () => {
                const str1 = `Xtime=[[1], [2], [3], [4], [5], [6], [7]]\n`;
                const str2 = `yamt=[[25000], [55000], [75000], [110000], [128000], [155000], [180000]]\n\n`;
                 
                const str3 = `regr = linear_model.LinearRegression()\n\n`;

                const str4 = `# Train the model using the training sets\n`;
                const str5 = `X=Xtime\n`;
                const str6 = `y=yamt\n`;
                const str7 = `regr.fit(X, y)\n\n`;

                const str8 = `# Make predictions using the testing set\n`;
                const str9 = `print(regr.predict([[10]]))\n\n`;
                
                const str10 = `%matplotlib inline\n`;
                const str11 = `import matplotlib.pyplot as plt\n`;
                const str12 = `plt.plot(Xtime, regr.predict(Xtime), 'b', X,y, 'k.')\n\n`;

                const scikitRun_linearRegressionStr = str1 + str2 + str3 + str4 + str5 + str6 + str7 + str8 + str9 + str10
                                                     +str11 + str12;
                JupyterNativeApi.SetCodeAndExecute(scikitRun_linearRegressionStr);
            });


            // 네이버 크롤링
            const search_naver_crawling = DocumentObjectModelApi.GetDom("#search-naver-crawling"); 
            const btn_naver_crawling = DocumentObjectModelApi.GetDom("#btn-naver-crawling");
            btn_naver_crawling.addEventListener('click', () => {
                const importStr = `import requests\nfrom bs4 import BeautifulSoup\n\n`;
                const search_keyword = search_naver_crawling.value;
                const search_url = `url = "https://search.naver.com/search.naver?where=news&sm=tab_jum&query={${search_keyword}}"\n\n`;

                const str2 = `r = requests.get(url)\nsoup = BeautifulSoup(r.text, 'html.parser')\nnews_titles = soup.select('.news .type01 li dt a[title]')\n\n`;
                const str3 = `print('총', len(news_titles), '개의 뉴스 제목이 있습니다')\n`;
                const str4 = `print()\n`;
                const str5 = `for title in news_titles:\n`
                const str6 = `    print(title['title'])\n`;

                const executedStr = importStr + search_url + str2 + str3 + str4 + str5 + str6;
                JupyterNativeApi.SetCodeAndExecute(executedStr);
            });
            this.m_TemplateDomButtonArr.push({
                name: "btn_naver_crawling",
                dom: btn_naver_crawling
            });

        }

        static GetTemplateDomButtonArr = () => {
            return this.m_TemplateDomButtonArr;
        } 

        static GetMainDom = () => {
            return this.m_MainDom;
        }

        static ToggleIsShowMainDom = () => {
            if(this.m_IsShowMainDom === true){
                this.m_MainDom.css("display" ,"none");
                this.m_IsShowMainDom = false;
            } else {
                this.m_MainDom.css("display" ,"flex");
                this.m_IsShowMainDom = true;
            }
        }
    }

    return SystemDomModel;
});
