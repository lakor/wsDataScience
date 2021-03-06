import handel_files
import svm_classify
import os
import csv
from collections import OrderedDict
import vectorize_full

header="../Data/"

# full feature list from file :
selectedFeatures=['BrowserVer','OsVer','Continent','OpName']
allFeatures = ['OpName','TimeStamp', 'Browser', 'BrowserVer', 'Os', 'OsVer', 'RoleInst', 'Continent', 'Country', 'Province', 'City' , 'Opid', 'Pid', 'Sid', 'IsFirst', 'Aid', 'Name', 'Success', 'Response', 'UrlBase', 'Host', 'ReqDuration']
numberOfClasses=2
svmModel={'kernel':'poly','C':1,'d':2,'gamma':2}

try:
    vectorize_full.run_code(header, allFeatures, numberOfClasses)

    def rewriteVectors(oldDir,newDir,newFeatures):
        for filename in os.listdir(oldDir):
            if "vectors" in filename:
                with open (oldDir+"/"+filename) as f:
                    data = list(csv.reader(f))
                f.close()
                with open (newDir+"/"+filename,'w') as f:
                    for vec in data:
                        for i in range(0,len(vec)):
                            if data[0][i] in newFeatures:
                                item=vec[i]
                                f.write("{0}".format(item))
                                if (i<len(vec)-1):
                                    f.write(',')
                        f.write('\n')
                    f.close()

    successDict=OrderedDict()
    for feature in allFeatures:
        newFeatures=list([item for item in selectedFeatures])
        if feature not in selectedFeatures:
            newFeatures.append(feature)
            newFeatures.append('Label')
            strF=str(newFeatures).replace(",",";")
            print(strF)
            rewriteVectors(header+"Train/TrainVectors",header+"Selection/FeatureSelection/TrainNewVectors",newFeatures)
            rewriteVectors(header+"Validation/ValidationVectors",header+"Selection/FeatureSelection/ValidationNewVectors",newFeatures)
            resultc=svm_classify.build_train_model(header+"Selection/FeatureSelection/TrainNewVectors",header+"Classify/SVM" ,svmModel,numberOfClasses)
            resultv=svm_classify.predict_validation_set(header+"Selection/FeatureSelection/ValidationNewVectors",header+"Classify/SVM")
            successDict[strF]=[resultc,resultv]

    successDict=OrderedDict(sorted(successDict.items(), key=lambda t: t[1]))

    def saveDictTofile():
        with open (header+"Selection/FeatureSelection/featureSelectionSum.csv",'w') as f:
            f.write("Added,Cross,Validation\n")
            for key in successDict:
                f.write("{0},{1},{2}\n".format(key,(successDict[key])[0],(successDict[key])[1]))
            f.close()

    saveDictTofile()

finally:
    # return data to rawData dir (when we want to start the procedure from the start)
    handel_files.return_files_from_train_test_to_rawdata(header+"RawData", header+"Train/TrainRawData", header+"Validation/ValidationRawData")
    print "\nfinished remove_files_to_rawdata"

    # remove all files from all directories at the end of the run
    handel_files.remove_all_files_from_all_folders(header)
    print "\nfinished removing all files from all directories"


