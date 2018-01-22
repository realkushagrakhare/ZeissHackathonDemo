import os
import cv2
import numpy as np 
from sklearn.cluster import KMeans
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
import time

from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings
import azure.common

block_blob_service = BlockBlobService(account_name='imagezeiss',account_key='eS2RdS7Zbt2WtejZfKzUQHXjihKds2c9YNjwo/G5RjtLhZK0k+hKbhdyWWtC5tTBL9TP+MAqK3VCiyzXlOtaIQ==')
n_clusters = 300#clusters for Kmean
trainImageCount = 0
train_labels = np.array([])
name_dict = {}
descriptor_list = []

def avg(inp):
	x=0
	y=0
	for i in inp:
		x=x+i[0]
		y=y+i[1]
	ans=[int(x/len(inp)),int(y/len(inp))]
	return ans

inp={}
inp["pos"]=[]
inp["neg"]=[]

images={}
images["pos"]=[]
images["neg"]=[]

size=[]

imageformat=".jpg"
path="./pos/"
imfilelist1=[os.path.join(path,f) for f in os.listdir(path) if f.endswith(imageformat)]
for i in imfilelist1:
	img=cv2.imread(i,0)
	bounded=img
	size.append(bounded.shape)
	inp["pos"].append(bounded)

path="./neg/"
imfilelist2=[os.path.join(path,f) for f in os.listdir(path) if f.endswith(imageformat)]
for j in imfilelist2:
	img=cv2.imread(j,0)
	bounded=img
	size.append(bounded.shape)
	inp["neg"].append(bounded)

dim=avg(size)

for i in inp["pos"]:
	resize=cv2.resize(i,(dim[1],dim[0]))
	images["pos"].append(resize)

for i in inp["neg"]:
	resize=cv2.resize(i,(dim[1],dim[0]))
	images["neg"].append(resize)

print "Done reading"

label_count = 0
count=0 
for word in images:
	name_dict[str(label_count)] = word
	sift_object = cv2.SIFT()#cv2.xfeatures2d.SIFT_create()
	for im in images[word]:
		train_labels = np.append(train_labels, label_count)
		kp, des = sift_object.detectAndCompute(im, None)
		descriptor_list.append(des)
		count+=1
	label_count += 1

print "No of labels ",label_count
print "Final image count ",count
descriptor_vstack = np.array(descriptor_list[0])

for remaining in descriptor_list:
	descriptor_vstack = np.vstack((descriptor_vstack, remaining))

print "Done description"
print np.shape(descriptor_vstack)

kmeans_obj = KMeans(n_clusters = n_clusters)
kmeans_ret = kmeans_obj.fit_predict(descriptor_vstack)
print "Kmeans cluster done"
n_images=count

mega_histogram = np.array([np.zeros(n_clusters) for i in range(n_images)])
old_count = 0
for i in range(n_images):
	l = len(descriptor_list[i])
	for j in range(l):
		idx = kmeans_ret[old_count+j]
		mega_histogram[i][idx] += 1.0
	old_count += l

scale = StandardScaler().fit(mega_histogram)
mega_histogram = scale.transform(mega_histogram)
print "Histogram transforming"

clf = SVC()

clf.fit(mega_histogram, train_labels)

print "Done Training"
print "Starting testing with clusters",n_clusters


#imageformat=".jpg"
#path="./"
val = 1
font = cv2.FONT_HERSHEY_SIMPLEX

while(True):
	try:
		block_blob_service.get_blob_to_path('uplink',"firstblood"+str(val)+".jpg","out"+str(val)+".jpg")
		img =cv2.imread("./"+"out"+str(val)+".jpg", 0)
		img1 =cv2.imread("./"+"out"+str(val)+".jpg", 1)
		if img is not None:
			im=cv2.resize(img,(dim[1],dim[0]))
			kp,des = sift_object.detectAndCompute(im, None)
			vocab = np.array([0 for i in range(n_clusters)])

			test_ret = kmeans_obj.predict(des)
			for each in test_ret:
				vocab[each] += 1
			vocab = vocab.reshape(1,-1)
			vocab = scale.transform(vocab)
			lb = clf.predict(vocab)
			if(name_dict[str(int(lb[0]))]=="pos"):
				print "Image is positive for Marburg virus"
				cv2.putText(img1,'Positive',(30,30), font, 1,(0,255,0),2)
			elif(name_dict[str(int(lb[0]))]=="neg"):
				print "Image is negative for Marburg virus"
				cv2.putText(img1,'Negative',(30,30), font, 1,(0,0,255),2)
			print "-------------------------------------------------------------------------------"
			cv2.imwrite("sendvr.jpg",img1)
			block_blob_service.create_blob_from_path('vrone',"yesno.jpg","sendvr.jpg")
			val = val + 1
			time.sleep(3)
	except azure.common.AzureMissingResourceHttpError:
		pass
	except:
		print "other error found"
