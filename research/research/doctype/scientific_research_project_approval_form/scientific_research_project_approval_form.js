frappe.ui.form.on("Scientific Research Project Approval Form", {
	refresh(frm) {

		let lang = frappe.boot.lang || "en";

		let header_html = "";

		if (lang === "en") {

			header_html = `
			<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@500&display=swap" rel="stylesheet">

			<div style="display:flex; align-items:center; justify-content:space-between;
						margin-bottom:12px; font-family:'Tajawal', sans-serif; color:#333;">

				<img src="/files/398187124_832924115292771_8632611931367621524_n.png"
					 style="width:150px; height:auto; margin-left:50px;">

				<div style="text-align:center; flex:1; font-size:20px; font-weight:bold; line-height:1.8;">
					Scientific Research Project Approval Form<br>
					For the academic year 2025/2026<br>
					<span style="font-size:20px;">
						University of Tal Afar / University Presidency
					</span>
				</div>

				<img src="/files/37171594305659483.png"
					 style="width:200px; height:auto; margin-right:50px;">
			</div>
			`;

		} else {

			header_html = `
			<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@500&display=swap" rel="stylesheet">

			<div style="display:flex; align-items:center; justify-content:space-between;
						margin-bottom:12px; font-family:'Tajawal', sans-serif; color:#333; direction:rtl;">

				<img src="/files/398187124_832924115292771_8632611931367621524_n.png"
					 style="width:150px; height:auto; margin-left:50px;">

				<div style="text-align:center; flex:1; font-size:20px; font-weight:bold; line-height:1.8;">
					استمارة اعتماد مشروع بحث علمي<br>
					للعام الدراسي 2026/2025<br>
					<span style="font-size:20px;">
						جامعة تلعفر / رئاسة الجامعة
					</span>
				</div>

				<img src="/files/37171594305659483.png"
					 style="width:200px; height:auto; margin-right:50px;">
			</div>
			`;
		}

		frm.set_df_property("form_header", "options", header_html);
		frm.refresh_field("form_header");
	}
});