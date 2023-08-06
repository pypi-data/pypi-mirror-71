define([
    "base/js/namespace"

], function(Jupyter) {

    const SetCodeAndExecute = (str) => {
        Jupyter.notebook.
            insert_cell_above('code').
            set_text(str);
        Jupyter.notebook.select_prev();
        Jupyter.notebook.execute_cell_and_select_below();
    }

    return {
        SetCodeAndExecute
    }
});