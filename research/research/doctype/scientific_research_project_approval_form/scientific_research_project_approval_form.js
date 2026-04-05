frappe.ui.form.on("Scientific Research Project Approval Form", {
    onload: function(frm) {
        frm.fields_dict["college"].df.only_select = 1;
        frm.fields_dict["department"].df.only_select = 1;
        frm.refresh_fields();

        frm.set_query("department", function() {
            if (!frm.doc.college) {
                return {
                    filters: {
                        name: "__no_results__"
                    }
                };
            }
            return {
                filters: {
                    college: frm.doc.college
                }
            };
        });
    },

    college: function(frm) {
        frm.set_value("department", "");

        frm.set_query("department", function() {
            if (!frm.doc.college) {
                return {
                    filters: {
                        name: "__no_results__"
                    }
                };
            }
            return {
                filters: {
                    college: frm.doc.college
                }
            };
        });
    }
});