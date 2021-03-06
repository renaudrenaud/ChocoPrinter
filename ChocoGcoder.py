# coding: utf-8

import sys, getopt
import time

class GCODER:
    """
    A class to modify GCODE specifically for chocolate prints

    specifically for our use, we want to manage code

    """
    def __init__(self, fileName):
        """
        fileName    : string, the complete file name to recode
        """
        self.fileName = fileName

    def recodeFile(self):
        """
        This method to recode the file
        """
        rv = "Cannot operate on file!"
        # let's try to open the file
        try:
            infile = open(self.fileName,'r') 
            data = infile.read()
            myList = data.splitlines()            
            infile.close()
        except:
            rv = "Cannot operate on file! Unable to open " + self.fileName
            
        if len(myList) > 0:

            # let us go for the move...

            newCode = list()

            currentE = float(0)
            valveIsOpen = False
            fgCopy = True
            for _, line in enumerate(myList):
                if ";" in line[0]:
                    newCode.append(line + chr(13))
                else:
                    if "M109" in line or "M104" in line:
                        newCode.append(";ChocGCoder has removed this line " + line + chr(13))
                        fgCopy = False
                    elif "G92 E0" in line:
                        currentE = float(0)
                        
                    elif "E" in line and "G92" not in line:
                        li = line.split()    
                        floatE = float(li[len(li)-1][1:])
                        if floatE > currentE and valveIsOpen is False:
                            newCode.append('M104 S255 ;open the valve ChocoGCoder' + chr(13))
                            newCode.append('G4 P200 ;wait 200ms ChocoGCoder' + chr(13))
                            valveIsOpen = True
                            
                        if floatE < currentE and valveIsOpen is True:
                            newCode.append('M104 S0 ;close the valve ChocoGCoder' + chr(13))
                            newCode.append('G4 P200 ;wait 200ms ChocoGCoder' + chr(13))
                            valveIsOpen = False 

                        currentE = floatE  # updating currentE

                    elif "E" not in line:        
                        if valveIsOpen is True:
                            newCode.append('M104 S0 ;close the valve ChocoGCoder' + chr(13))
                            newCode.append('G4 P200 ;wait 200ms ChocoGCoder' + chr(13))
                            currentE = floatE
                            valveIsOpen = False
                    
                    if fgCopy is True:
                        newCode.append(line + chr(13))
                    
                    fgCopy = True



            # manage file name to generate export file

            timestr = time.strftime("%Y%m%d-%H%M%S")
            newFileName = self.fileName[:len(self.fileName)-6] + "_" + timestr + '.gcode' 

            outFile = open(newFileName,'w') 
            rv = newFileName

            outFile.writelines(newCode)
            outFile.close()        

        return rv    



def help():
    print ("----------------------")
    print ("    Choco GCODER 1.0")
    print ("----------------------")
    print ("_____________,-.___     _")
    print ("|____        { {]_]_]   [_]")
    print ("|___ `-----.__\ \_]_]_    . `")
    print ("|   `-----.____} }]_]_]_   ,")
    print ("|_____________/ {_]_]_]_] , ` ")
    print ('              `-"')
    print ('')
    print ('A script to recode GCODE')
    print ('for chocolate printing')
    print ('')
    print ('Usage:')
    print (">>>python ChocoGCoder fileNameToModify")


def main(argv):
    """Recode GCODE File"""
    fileName = ""
    
    fileName = argv[0]
    
    # fileName = "Z:\\Impression 3D\\Fichier Objets 3D\\Chocolate printer\\files\\CFFFP_chocolate_v2.gcode"
    if fileName =='':
        help()
        sys.exit(0)

    import os
    cwd = os.getcwd()

    fileName = cwd + '\\' + fileName
    myChoco = GCODER(fileName)
    
    print ('Done >' +  myChoco.recodeFile())

if __name__ == "__main__":
    main(sys.argv[1:])   