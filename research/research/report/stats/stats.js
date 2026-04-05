// Copyright (c) 2026, obaida and contributors
// For license information, please see license.txt

frappe.query_reports["Stats"] = {
	filters: [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			reqd: 0,
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
			reqd: 0,
		},
		{
			fieldname: "research_type",
			label: __("Research Type"),
			fieldtype: "Select",
			options: "\nAcademic\nApplied\nAcademic and Applied",
			reqd: 0,
		},
		{
			fieldname: "researcher_name",
			label: __("Researcher Name"),
			fieldtype: "Data",
			reqd: 0,
		},
	],

	formatter: function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		if (column.fieldname === "research_status") {
			if (data && data.research_status === "Completed") {
				value = `<span style="color: green; font-weight: bold;">${value}</span>`;
			} else if (data && data.research_status === "Planned") {
				value = `<span style="color: orange; font-weight: bold;">${value}</span>`;
			} else if (data && data.research_status === "Post") {
				value = `<span style="color: blue; font-weight: bold;">${value}</span>`;
			}
		}

		return value;
	},
};