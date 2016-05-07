# coding: utf-8

import os
import random
import shutil

# move all files from daily folders to one folder,
# each files name according to the folder (day) he came from
def move_data_to_one_folder(dataFolder, rawdatafolder):
    for foldername in os.listdir(dataFolder):
        try:
            filePath = dataFolder + "/" + foldername + "/requests.csv"
            destPath = rawdatafolder + "/" + foldername + ".csv"
            shutil.move(filePath, destPath)
        except:
            print "request file not exist in folder: " + foldername

# move random 90% of the data files to TrainData directory.
# the rest to TestData.
# this way they won't have an affect on feature selection.
def split_files_to_test_and_train_dir(rawdataDirPath, trainDirPath, validationDirPath):
    for filename in os.listdir(rawdataDirPath):
        prob = random.random()
        if prob < 0.8 and "empty" not in filename:
            filePath = rawdataDirPath + "/" + filename
            destPath = trainDirPath + "/" + filename
            shutil.move(filePath, destPath)

    for filename in os.listdir(rawdataDirPath):
        if "empty" not in filename:
            filePath = rawdataDirPath + "/" + filename
            destPath = validationDirPath + "/" + filename
            shutil.move(filePath, destPath)


# remove files from validation and train directories to rawData.
def return_files_from_train_test_to_rawdata(rawdataDirPath, validationDirPath, trainDirPath):
    for filename in os.listdir(validationDirPath):
        if "empty" not in filename:
            filePath = validationDirPath + "/" + filename
            destPath = rawdataDirPath + "/" + filename
            shutil.move(filePath, destPath)

    for filename in os.listdir(trainDirPath):
        if "empty" not in filename:
            filePath = trainDirPath + "/" + filename
            destPath = rawdataDirPath + "/" + filename
            shutil.move(filePath, destPath)


def delete_files_from_dir(dirPath):
    for filename in os.listdir(dirPath):
        if "empty" not in filename:
            filePath = dirPath + "/" + filename
            os.remove(filePath)