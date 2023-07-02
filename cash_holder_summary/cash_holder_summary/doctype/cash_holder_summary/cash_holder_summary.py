# Copyright (c) 2023, Kitti U. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class CashHolderSummary(Document):

    def submit(self):
        if (self.opening + self.deposit - self.withdrawal) != self.closing:
            frappe.throw(_("Invalid entries or closing amount."))
        super(CashHolderSummary, self).submit()

    @property
    def opening(self):
        gle = frappe.db.sql(
            """
                select sum(debit) - sum(credit) from `tabGL Entry`
                where posting_date < %(date_from)s and account = %(account)s and is_cancelled = 0
            """,
            values={"date_from": self.date_from, "account": self.cash_account},
            as_dict=0,
        )
        return gle[0][0] or 0

    @property
    def closing(self):
        gle = frappe.db.sql(
            """
            select sum(debit) - sum(credit) from `tabGL Entry`
            where posting_date <= %(date_to)s and account = %(account)s and is_cancelled = 0
            """,
            values={"date_to": self.date_to, "account": self.cash_account},
            as_dict=0,
        )
        return gle[0][0] or 0

    @property
    def deposit(self):
        return sum([r.debit for r in self.entries])

    @property
    def withdrawal(self):
        return sum([r.credit for r in self.entries])

@frappe.whitelist()
def get_entries(account=False, date_from=False, date_to=False):
    if not (account and date_from and date_to):
        return []
    ret = frappe.db.sql(
        """
        select voucher_type, voucher_no, posting_date, remarks,
        case when sum(debit-credit) > 0 then sum(debit-credit) else 0 end as debit,
        case when sum(credit-debit) > 0 then sum(credit-debit) else 0 end as credit
        from `tabGL Entry`
        where account=%s
        and posting_date >= %s and posting_date <= %s
        and is_cancelled = 0
        group by voucher_type, voucher_no, posting_date, remarks
        order by posting_date, voucher_no
        """,
        (account, date_from, date_to),
        as_dict=1,
    )
    return ret