from sonarqube import SonarQubeClient
import json

url = "https://<URL>"
username = "admin"
password = "<PASS>"
sonar = SonarQubeClient(sonarqube_url=url, username=username, password=password)

paling_banyak = 0
total = 0
project = list(sonar.projects.search_projects())
branch = ""

with open("loc.csv", "a") as file_object:
	file_object.seek(0)
	for i in range(0,len(project)):
		projects = project[i]['key']
		nama_project = project[i]['name']
		loc = sonar.project_branches.search_project_branches(project=projects)
		#print("Project : ", projects, "\nNama : ",nama_project,"\n\n")
		if len(loc['branches']) > 0 :
			for j in range(0,len(loc['branches'])):
				component = sonar.measures.get_component_with_specified_measures(component=projects, branch=loc['branches'][j]['name'],metricKeys="ncloc")
				branch = loc['branches'][j]['name']
				if component['component']['measures'] :
					#print("Branch : " , loc['branches'][j]['name'], "\t:" , component['component']['measures'][0]['value'])
					if paling_banyak < int(component['component']['measures'][0]['value']) :
						paling_banyak = int(component['component']['measures'][0]['value'])
						branch = loc['branches'][j]['name']
			#print('-'*50)
			#print("LOC TERBANYAK : ", paling_banyak, "(",branch,")")
			tes = nama_project+","+projects+","+branch+","+str(paling_banyak)+","
			print(nama_project+","+projects+","+branch+","+str(paling_banyak)+",")
			file_object.write(tes)
			file_object.write("\n")
			total += paling_banyak
			paling_banyak = 0
		else:
			component = sonar.measures.get_component_with_specified_measures(component=projects, branch=loc['branches'][0]['name'],metricKeys="ncloc")
			#print("Branch : " , loc['branches'][0]['name'], ":".ljust(50) , component['component']['measures'][0]['value'])
			tess = nama_project+","+projects+","+branch+","+str(paling_banyak)+","
			print(nama_project+","+projects+","+branch+","+str(paling_banyak)+",")
			file_object.write(tess)
			file_object.write("\n")
file_object.close()
print('='*50)
print("TOTAL LOC : ", total)
print('='*50)
