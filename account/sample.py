import os
module_dir = os.path.dirname(__file__)  # get current directory
file_path = os.path.join(module_dir, '../static/kenya/counties.txt')
# file_path = os.path.join(module_dir, '../static/text/subcounties.txt')
file_path_to_county = os.path.join(module_dir,'../static/kenya/counties.txt')
file_path_to_subcounty = os.path.join(module_dir,'../static/kenya/subcounties.txt')
file_path_to_tribes = os.path.join(module_dir,'../static/kenya/tribes in kenya.txt')
file_path_to_divisions = os.path.join(module_dir,'../static/kenya/divisions.txt')
file_path_to_courses = os.path.join(module_dir,'../static/kenya/courses.txt')
file_path_to_education = os.path.join(module_dir,'../static/kenya/campuses.txt')

file = open(file_path,"r")
county=file.readlines()
file.close()
new_county=[]
for county in county:
    new_county.append(county.replace("\n",""))

new_county_1=[]
for county in new_county:
    new_county_1.append((county,county))

file = open(file_path_to_subcounty,"r")
sub_details = file.readlines()
file.close()
new_sub_details = []
for subcounty in sub_details:
    new_sub_details.append(subcounty.replace("\n",""))
new_sub_details_1 = []
for subcounty in new_sub_details:
    new_sub_details_1.append((subcounty,subcounty))

file = open(file_path_to_tribes,"r")
tribes = file.readlines()
file.close()
new_tribes = []
for tribe in tribes:
    new_tribes.append(tribe.replace("\n",""))
new_tribes_1 = []
for tribe in new_tribes:
    new_tribes_1.append((tribe,tribe))

file = open(file_path_to_divisions,"r")
divisions = file.readlines()
file.close()
new_division = []
for div in divisions:
    new_division.append(div.replace("\n",""))
new_divisions_1 = []
for div in new_division:
    new_divisions_1.append((div,div))

file = open(file_path_to_courses,"r")
courses = file.readlines()
file.close()
new_courses = []
for course in courses:
    new_courses.append(course.replace("\n",""))
new_courses_1 = []
for course in new_courses:
    new_courses_1.append((course,course))

file = open(file_path_to_education,"r")
education = file.readlines()
file.close()
new_education = []
for edu in education:
    new_education.append(edu.replace("\n",""))
new_education_1 = []
for edu in new_education:
    new_education_1.append((edu,edu))