from datetime import timedelta

import frappe
import datetime
from frappe.utils import flt, cint

@frappe.whitelist()
def get_dashboards(club=None):
	if not club:
		return None 
		
	project_stats = frappe.get_all("Project",
		filters={"club": club, "docstatus": 1},
		fields=["""count(name) as project_count, sum(incomes) as income, sum(expenditure) as expense, 
			sum(total) as footfall, sum(TIMEDIFF(end_time, start_time)) as total_time"""])

	meeting_stats = frappe.get_all("Meeting",
		filters={"club": club, "docstatus": 1},
		fields=["count(name) as meeting_count, sum(TIMEDIFF(end_time, start_time)) as total_time"])
	
	top_projects = frappe.get_all("Project",
		filters={"club": club, "docstatus": 1},
		fields=["name","project_name", "avenue_1", "avenue_2", "(incomes - expenditure) as net_profit"],
		order_by="net_profit desc",
		limit=5)

	reporting_status = frappe.get_all("Project",
		filters={"club": club, "docstatus": 1},
		fields=["project_status as status", "count(name) as count"],
		group_by="status")

	projects_by_month = frappe.get_all("Project",
		filters={"club": club, "docstatus": 1},
		fields=["month(end_time) as month", "count(name) as count"],
		group_by="month", order_by="month")
	
	current_month = datetime.datetime.now().strftime("%B")
	reporting_months = []
	for month in ['July', 'August', 'September', 'October', 'November',
		'December','January','Febuary','March', 'April', 'May', 'June']:
			reporting_months.append(month)
			if month == current_month:
				break;
	
	club_service_count, com_service_count, isd_count, pd_count, hrd_count = [],[],[],[], []
	sports_count, ed_count, pr_count, editorial_count, web_com_count, pis_count = [],[],[],[],[],[]

	club_service_total_time, com_service_total_time, isd_total_time, pd_total_time, hrd_total_time = [],[],[],[], []
	sports_total_time, ed_total_time, pr_total_time, editorial_total_time, web_com_total_time, pis_total_time = [],[],[],[],[],[]

	for month in reporting_months:
		club_service = com_service = isd = pd = sports = ed = pr = editorial = web_com = pis = hrd = 0 
		club_service_time = com_service_time = isd_time = pd_time = sports_time = 0
		ed_time = pr_time = editorial_time = web_com_time = pis_time = hrd_time = 0 
		
		projects = get_club_projects(club, month)
		if projects:
			for project in projects:
				avenue = [project.avenue_1, project.avenue_2]
				if "Club Service" in avenue:
					club_service+=1
					club_service_time+=cint(project.total_time) //3600
				if  "Community Service" in avenue:
					com_service+=1
					com_service_time+=cint(project.total_time) //3600
				if "International Service" in avenue:
					isd+=1
					isd_time+=cint(project.total_time) //3600
				if "Professional Development" in avenue:
					pd+=1
					pd_time+=cint(project.total_time) //3600
				if "Sports" in avenue:
					sports+=1
					sports_time+=cint(project.total_time) //3600
				if "ED" in avenue:
					ed+=1
					ed_time+=cint(project.total_time) //3600
				if "PR" in avenue:
					pr+=1
					pr_time+=cint(project.total_time) //3600
				if "Editorial" in avenue:
					editorial+=1
					editorial_time+=cint(project.total_time) //3600
				if "Web Communications" in avenue:
					web_com+=1
					web_com_time+=cint(project.total_time) //3600
				if "PIS" in avenue:
					pis+=1
					pis_time+=cint(project.total_time) //3600
				if avenue == "HRD":
					hrd+=1
					hrd_time+=cint(project.total_time) //3600

		club_service_count.append(club_service)
		com_service_count.append(com_service)
		isd_count.append(isd)
		pd_count.append(pd)
		sports_count.append(sports)
		ed_count.append(ed)
		pr_count.append(pr)
		editorial_count.append(editorial)
		web_com_count.append(web_com)
		pis_count.append(pis)
		hrd_count.append(hrd)

		club_service_total_time.append(club_service_time)
		com_service_total_time.append(com_service_time)
		isd_total_time.append(isd_time)
		pd_total_time.append(pd_time)
		sports_total_time.append(sports_time)
		ed_total_time.append(ed_time)
		pr_total_time.append(pr_time)
		editorial_total_time.append(editorial_time)
		web_com_total_time.append(web_com_time)
		pis_total_time.append(pis_time)
		hrd_total_time.append(hrd_time)

	projects_per_month = {
		'Club Service' : club_service_count,
		'Community Service' : com_service_count,
		'International Service' : isd_count,
		'Professional Development' : pd_count,
		'Sports' : sports_count,
		'ED' : ed_count,
		'PR' : pr_count,
		'Editorial' : editorial_count,
		'Web Communications' : web_com_count,
		'PIS' : pis_count,
		'HRD' : hrd_count
	}

	projects_time_per_month = {
		'Club Service' : club_service_total_time,
		'Community Service' : com_service_total_time,
		'International Service' : isd_total_time,
		'Professional Development' : pd_total_time,
		'Sports' : sports_total_time,
		'ED' : ed_total_time,
		'PR' : pr_total_time,
		'Editorial' : editorial_total_time,
		'Web Communications' : web_com_total_time,
		'PIS' : pis_total_time,
		'HRD' : hrd_total_time
	}

	return {
		"total_income": project_stats[0].income,
		"total_expenses": project_stats[0].expense,
		"net_profit": flt(project_stats[0].income) - flt(project_stats[0].expense),
		"total_footfall": cint(project_stats[0].footfall),
		"total_projects": project_stats[0].project_count,
		"total_project_time": cint(project_stats[0].total_time) // 3600,
		"total_meetings":  cint(meeting_stats[0].meeting_count),
		"total_meeting_time": cint(meeting_stats[0].total_time) // 3600,
		"top_projects": top_projects,
		"reporting_status": reporting_status,
		"projects_per_month": projects_per_month,
		"projects_time_per_month": projects_time_per_month,
		"reporting_months": reporting_months
	}

def get_club_projects(club, month):
	projects = frappe.get_all("Project",
		filters={"club": club, "reporting_month": month, "docstatus": 1},
		fields=["avenue_1", "avenue_2", "CONVERT(TIMEDIFF(end_time, start_time), UNSIGNED) as total_time"])
	return projects

