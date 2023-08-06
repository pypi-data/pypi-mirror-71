/**
* ----------------------------------------------------------------------------
* Copyright (c) 2020 - Lee Jin Yong
* copyright (c) 2020 - Company Black Logic
* ----------------------------------------------------------------------------
*/

define([
    "require",
    "jquery",
    "base/js/namespace",
    "base/js/events",
    'codemirror/lib/codemirror',

    "nbextensions/visualpython/Source/FrontEndApi/Index",
    "nbextensions/visualpython/Source/SystemModel/Index",
],  function(
    Requirejs,
    $,
    Jupyter,
    Events,
    Codemirror,

    FrontEndApis,
    SystemModels
) {
    "use_strict";

    Jupyter.notebook.keyboard_manager.disable();

    const SystemDomModel = SystemModels.SystemDomModel;

    $('<link rel="stylesheet" type="text/css">')
        .attr('href', Requirejs.toUrl('./StaticFile/CSS/Index.css'))
        .appendTo('head');

    $('#site').css('position',"relative");
    $(`<div class="MainContainer-container"></div>`)
        .load(Jupyter.notebook.base_url + "nbextensions/visualpython/MainLayout.html", function (response, status, xhr) {
            if (status === "error") {
                alert(xhr.status + " " + xhr.statusText);
            }

            SystemDomModel.InitializeSystemDom();
        })
        .appendTo('#site');

    Jupyter.toolbar.add_buttons_group([{
        label: 'AI Visual Python',
        icon: 'fa-text-width',
        callback: () => {
            SystemDomModel.ToggleIsShowMainDom();
        }
    }]);

});
