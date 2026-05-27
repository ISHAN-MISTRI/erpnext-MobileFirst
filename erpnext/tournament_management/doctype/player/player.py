import frappe
from frappe.model.document import Document

class Player(Document):
	def on_update(self):
		# Update both the previous team and the new team counts
		old_doc = self.get_doc_before_save()
		if old_doc and old_doc.team != self.team:
			self.update_players_count_for_team(old_doc.team)
		self.update_players_count_for_team(self.team)

	def on_trash(self):
		# When deleting, the count needs to be updated with offset=-1
		self.update_players_count_for_team(self.team, offset=-1)

	def update_players_count_for_team(self, team_name, offset=0):
		if not team_name:
			return
		count = frappe.db.count("Player", filters={"team": team_name})
		if offset != 0:
			count = max(0, count + offset)
		frappe.db.set_value("Team", team_name, "players_count", count)
