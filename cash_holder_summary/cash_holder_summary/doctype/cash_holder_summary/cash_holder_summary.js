// Copyright (c) 2023, Kitti U. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Cash Holder Summary', {

	refresh(frm) {
	    frm.set_query("cash_account", function() {
            return {
				filters: {
				    account_type: "Cash",
					company: frm.doc.company
				}
            }
        })

		// Button to Top Up - Create Payment Entry
		if(frm.doc.docstatus==1) {
			frm.add_custom_button(__("Top Up"), function () {
				frappe.route_options = {
					"payment_type": "Internal Transfer",
					"paid_to": frm.doc.cash_account,
					"cash_holder_summary": frm.doc.name
				};
				frappe.set_route("payment-entry", "new-payment-entry");
			});
		}
	},

	date_from: function(frm) {
		get_cash_holder_entries(frm)
	},
	date_to: function(frm) {
		get_cash_holder_entries(frm)
	},
	cash_account: function(frm) {
		get_cash_holder_entries(frm)
	},

});

function get_cash_holder_entries(frm) {
	frappe.call({
		method:
			"cash_holder_summary.cash_holder_summary.doctype.cash_holder_summary.cash_holder_summary.get_entries",
		args: {
			account: frm.doc.cash_account,
			date_from: frm.doc.date_from,
			date_to: frm.doc.date_to,
		},
		callback: (r) => {
			frm.set_value("entries", r.message)
		},
	});
}