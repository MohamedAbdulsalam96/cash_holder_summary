frappe.listview_settings['Cash Holder Summary'] = {

	onload: function(listview) {
		if (listview.page.fields_dict.cash_account) {
			listview.page.fields_dict.cash_account.get_query = function() {
				return {
					"filters": {
						account_type: "Cash"
					}
				};
			};
		}
	},

	hide_name_column: false
};
