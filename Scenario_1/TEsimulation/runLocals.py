import subprocess as sub
import os

numref = int(input("How many reference blocks? "))
#number = []
number = [int(input("Number of next reference block: ")) for zz in range(numref)]


buildings = ["roomb{}".format(str(jj)) for jj in number]
controls = ["ctrlb{}".format(str(jj)) for jj in number]
hsubstations = ["hsubb{}".format(str(jj)) for jj in number]
heatpumps = ["hpb{}".format(str(jj)) for jj in number]
thermalstorages = ["tesb{}".format(str(jj)) for jj in number]
elbackups = ["ebb{}".format(str(jj)) for jj in number]
elsubstations = ["esubb{}".format(str(jj)) for jj in number]
#dhsubstations = ["hnsubb{}".format(str(jj)) for jj in number]
elappliances = ["eab{}".format(str(jj)) for jj in number]

print(buildings)
cwd = os.getcwd() #"C:\GitHub_Projects\ModelicaTest\Test_Room1\\test_ZerOBNL" #os.getcwd() #Current directory

for building in buildings:

    os.chdir(cwd+"\TMP_FOLDER\{}".format(building))

    
    sub.Popen(["python", "wrapper.py"])
	
for control in controls:
	
    os.chdir(cwd+"\TMP_FOLDER\{}".format(control))
	
    sub.Popen(["python", "wrapper.py"])
	
for hsubstation in hsubstations:
	
    os.chdir(cwd+"\TMP_FOLDER\{}".format(hsubstation))
	
    sub.Popen(["python", "wrapper.py"])
	
for heatpump in heatpumps:
	
    os.chdir(cwd+"\TMP_FOLDER\{}".format(heatpump))
	
    sub.Popen(["python", "wrapper.py"])	

for thermalstorage in thermalstorages:
	
    os.chdir(cwd+"\TMP_FOLDER\{}".format(thermalstorage))
	
    sub.Popen(["python", "wrapper.py"])
	

for elbackup in elbackups:
	
    os.chdir(cwd+"\TMP_FOLDER\{}".format(elbackup))
	
    sub.Popen(["python", "wrapper.py"])
	
for elsubstation in elsubstations:
	
    os.chdir(cwd+"\TMP_FOLDER\{}".format(elsubstation))
	
    sub.Popen(["python", "wrapper.py"])	

#for dhsubstation in dhsubstations:
	
#    os.chdir(cwd+"\TMP_FOLDER\{}".format(dhsubstation))
	
#    sub.Popen(["python", "wrapper.py"])
	
for elappliance in elappliances:
	
    os.chdir(cwd+"\TMP_FOLDER\{}".format(elappliance))
	
    sub.Popen(["python", "wrapper.py"])
	
	
os.chdir(cwd+"\TMP_FOLDER\grid")
	
sub.Popen(["python", "wrapper.py"])
	
os.chdir(cwd+"\TMP_FOLDER\dhnet")
	
sub.Popen(["python", "wrapper.py"])
	
