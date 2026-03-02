# Copyright (c) 2026, obaida and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    filters = filters or {}
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {
            "label": _("Research Title"),
            "fieldname": "research_title",
            "fieldtype": "Data",
            "width": 220,
        },
        {
            "label": _("Research"),
            "fieldname": "research",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": _("Date of Application"),
            "fieldname": "date_of_application",
            "fieldtype": "Date",
            "width": 120,
        },
        {
            "label": _("Submission Date"),
            "fieldname": "submission_date",
            "fieldtype": "Date",
            "width": 120,
        },
        {
            "label": _("Research Type"),
            "fieldname": "research_type",
            "fieldtype": "Data",
            "width": 140,
        },
        {
            "label": _("Research Nature"),
            "fieldname": "research_nature",
            "fieldtype": "Data",
            "width": 140,
        },
        {
            "label": _("Research Status"),
            "fieldname": "research_status",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": _("Research Plan"),
            "fieldname": "research_plan",
            "fieldtype": "Data",
            "width": 130,
        },
        {
            "label": _("Name of Journal"),
            "fieldname": "name_of_journal",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": _("Journal Type"),
            "fieldname": "journal_type_copy",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": _("Date of Acceptance"),
            "fieldname": "date_of_acceptance",
            "fieldtype": "Date",
            "width": 130,
        },
        {
            "label": _("Research Summary"),
            "fieldname": "research_summary",
            "fieldtype": "Data",
            "width": 200,
        },
    ]


def get_data(filters):
    conditions = get_conditions(filters)

    data = frappe.db.sql(
        """
        SELECT
            doc.name,
            doc.research_title,
            doc.research,
            doc.date_of_application,
            doc.submission_date,
            doc.research_type,
            doc.research_nature,
            doc.research_status,
            doc.research_plan,
            doc.name_of_journal,
            doc.journal_type_copy,
            doc.date_of_acceptance,
            doc.research_summary
        FROM
            `tabScientific Research Project Approval Form` doc
        WHERE
            1=1
            {conditions}
        ORDER BY
            doc.date_of_application DESC
    """.format(
            conditions=conditions
        ),
        filters,
        as_dict=True,
    )

    # Attach researcher names to each row
    for row in data:
        researchers = frappe.db.sql(
            """
            SELECT researcher_name
            FROM `tabResearcher`
            WHERE parent = %s
        """,
            row["name"],
            as_dict=True,
        )
        row["researchers"] = ", ".join(
            [r.get("researcher_name", "") for r in researchers if r.get("researcher_name")]
        )

    return data


def get_conditions(filters):
    conditions = ""

    if filters.get("from_date"):
        conditions += " AND doc.date_of_application >= %(from_date)s"

    if filters.get("to_date"):
        conditions += " AND doc.date_of_application <= %(to_date)s"

    if filters.get("research_type"):
        conditions += " AND doc.research_type = %(research_type)s"

    if filters.get("researcher_name"):
        conditions += """ AND EXISTS (
            SELECT 1 FROM `tabResearcher` r
            WHERE r.parent = doc.name
            AND r.researcher_name LIKE %(researcher_name)s
        )"""
        filters["researcher_name"] = "%" + filters["researcher_name"] + "%"

    return conditions


def get_chart_data(filters, data):
    """Optional: returns chart data for visual display"""
    type_counts = {}
    for row in data:
        t = row.get("research_type") or "Unknown"
        type_counts[t] = type_counts.get(t, 0) + 1

    return {
        "data": {
            "labels": list(type_counts.keys()),
            "datasets": [{"values": list(type_counts.values())}],
        },
        "type": "donut",
        "colors": ["#5e64ff", "#743ee2", "#ff5858"],
    }


def get_summary(filters, data):
    """Summary cards shown at the top of the report"""
    total = len(data)

    # Count unique researchers
    all_researchers = set()
    for row in data:
        if row.get("researchers"):
            for r in row["researchers"].split(", "):
                all_researchers.add(r.strip())

    academic = sum(1 for r in data if r.get("research_type") == "Academic")
    applied = sum(1 for r in data if r.get("research_type") == "Applied")
    academic_applied = sum(1 for r in data if r.get("research_type") == "Academic and Applied")
    completed = sum(1 for r in data if r.get("research_status") == "Completed")
    planned = sum(1 for r in data if r.get("research_status") == "Planned")
    posted = sum(1 for r in data if r.get("research_status") == "Post")

    return [
        {"value": total, "label": _("Total Research"), "datatype": "Int", "color": "blue"},
        {"value": len(all_researchers), "label": _("Total Researchers"), "datatype": "Int", "color": "green"},
        {"value": academic, "label": _("Academic"), "datatype": "Int", "color": "purple"},
        {"value": applied, "label": _("Applied"), "datatype": "Int", "color": "orange"},
        {"value": academic_applied, "label": _("Academic & Applied"), "datatype": "Int", "color": "cyan"},
        {"value": completed, "label": _("Completed"), "datatype": "Int", "color": "green"},
        {"value": planned, "label": _("Planned"), "datatype": "Int", "color": "yellow"},
        {"value": posted, "label": _("Posted"), "datatype": "Int", "color": "blue"},
    ]