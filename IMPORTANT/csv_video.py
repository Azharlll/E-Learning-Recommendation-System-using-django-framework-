import csv
import random
Firstname = ["user11","user31","user32","user33","user34","user35","user36","user37","user38","user39","user12","user13","user14","user15","user16","user17","user18","user19","user20","user21","user22","user23","user24","user25","user26","user27","user28","user29","user30","user40","user41","user42","user43","user44","user45","user46","user47","user48","user49","user50","user51","user52","user53","user54","user55","user56","user57","user58","user59","user60","user61","user62","user63","user64","user65","user66","user67","user68","user69","user70","user71","user72","user73","user74","user75","user76","user77","user78","user79","user80","user81","user82","user83","user84","user85","user86","user87","user88","user89","user90","user91","user92","user93","user94","user95","user96","user97","user98","user99","user100","user101","user102","user103","user104","user105","user106","user107","user108","user109"]

v_seeking = random.randint(0,10)
v_pauses = random.randint(0,10)
v_replay = random.randint(0,10)

a_seeking = random.randint(0,10)
a_pauses = random.randint(0,10)
a_replay = random.randint(0,10)

p_seeking = random.randint(0,10)
p_pauses = random.randint(0,10)
p_replay = random.randint(0,10)

myFile = open('useractivity.csv', 'w')
myData = []
for item in Firstname:
    v_seeking = random.randint(0,10)
    v_pauses = random.randint(0,10)
    v_replay = random.randint(0,10)

    a_seeking = random.randint(0,10)
    a_pauses = random.randint(0,10)
    a_replay = random.randint(0,10)

    p_seeking = random.randint(0,10)
    p_pauses = random.randint(0,10)
    p_replay = random.randint(0,10)

    tmp = [item,v_seeking,v_pauses,v_replay,a_seeking,a_pauses,a_replay,p_seeking,p_pauses,p_replay]
    myData.append(tmp)


with myFile:
    writer = csv.writer(myFile)
    writer.writerows(myData)

print("Writing complete")