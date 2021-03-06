import handel_files
import svm_classify
import vectorize_full

header="../Data/"

# full feature list from file :
selectedFeatures=['BrowserVer','OsVer','Country','OpName']
numberOfClassesOpt=[2,3,4]
selectedModels=[{'kernel': 'linear', 'C': 1, 'd': 1, 'gamma': 2},{'kernel': 'linear', 'C': 10, 'd': 1, 'gamma': 2}
                ,{'kernel': 'poly', 'C': 1, 'd': 1, 'gamma': 'auto'},{'kernel':'poly','C':1,'d':2,'gamma':'auto'},
                 {'kernel':'poly','C':1,'d':1,'gamma':2},{'kernel':'poly','C':1,'d':2,'gamma':2},{'kernel':'poly','C':10,'d':2,'gamma':2}]

try:

    with open (header+"Selection/ModelSelection/modelSelectionSum.csv",'w') as f:
        f.write("Model,Success\n")
        for numberOfClasses in numberOfClassesOpt:
            vectorize_full.run_code(header, selectedFeatures, numberOfClasses)
            for svmModel in selectedModels:
                try:
                    strLine=str(svmModel)+" Num Classes={0}".format(numberOfClasses)
                    print (strLine+"\n")
                    svm_classify.build_train_model(header+"Train/TrainVectors",header+"Classify/SVM" ,svmModel,numberOfClasses)
                    result=svm_classify.predict_validation_set(header+"Validation/ValidationVectors",header+"Classify/SVM")
                    f.write("{0},{1}\n".format(strLine,result))
                except:
                    print ("Failed: "+str(svmModel)+"\n")
                    continue
            handel_files.return_files_from_train_test_to_rawdata(header+"RawData", header+"Train/TrainRawData", header+"Validation/ValidationRawData")
            handel_files.remove_all_files_from_all_folders(header)
        f.close()

finally:
    # return data to rawData dir (when we want to start the procedure from the start)
    handel_files.return_files_from_train_test_to_rawdata(header+"RawData", header+"Train/TrainRawData", header+"Validation/ValidationRawData")
    print "\nfinished remove_files_to_rawdata"

    # remove all files from all directories at the end of the run
    handel_files.remove_all_files_from_all_folders(header)
    print "\nfinished removing all files from all directories"


