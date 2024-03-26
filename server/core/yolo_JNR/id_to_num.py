import os

# mappingFile=r'.\results\JNR\id_num.txt'
# motPath=r'.\MOT_File\track_id.txt'
# outFile=r'.\results\JNR\mot.txt'


def id_to_num(mappingFile,motPath,outFile):
    refInfo={}
    refFile=open(mappingFile,'r')
    refLst = refFile.read().split('\n')
    refFile.close()
    if not os.path.exists(os.path.dirname(outFile)):
        os.makedirs(os.path.dirname(outFile),0o777)

    outfile=open(outFile,'w')


    for ref in refLst:
        if ref!='':
            tkid,jeNum=ref.split(' ')
            # if jeNum in selectNum:
            refInfo[tkid]=jeNum


    motFile=open(motPath,'r')
    motLst=motFile.read().split('\n')
    motFile.close()

    for mot in motLst:
        if mot !='':
            frame,tkid,left, top, width, height,_,_,_=mot.split(' ')
            if jersey := refInfo.get(tkid):
                frame=int(frame)
                outfile.write('{} {} {} {} {} {} 1 1 1\n'.format(frame,jersey,left, top, width, height))
                continue
    outfile.close()