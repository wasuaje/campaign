# -*- coding: utf-8 -*-
import os,glob,decimal


FILESPATH="/home/wasuaje/Documentos/desarrollo/campaign/logs"
#campaignstats[306 - Empleo Oportunidades Personas]=[total,enviados,malos]
campaignstats={}

def sortedDictValues2(adict):
    keys = adict.keys()
    keys.sort()
    return keys

def read_file(thefile):
    if os.path.exists(thefile):
        file = open(thefile, "r")
        data = file.read()
        file.close()            
    else:
        print "archivo no existe"
        data=""
    return data

def sumarize(name,total,bad,good):
    
    if name in campaignstats: 
        campaignstats[name][0]+=total
        campaignstats[name][1]+=bad
        campaignstats[name][2]+=good
    else:        
        campaignstats[name]=[total,bad,good]
    
    return campaignstats
    
def gather_data(data):
    data=data.split('\n')
    #print data
    for i in data:
        i=i.replace('\r','')
        i=i.replace(':','')
        if 'Campaign ID' in i:
            cp_id=i.replace('Campaign ID','')            
            cp_id=cp_id.strip()
            #print cp_id
        if 'Campaign name' in i:
            cp_name=i.replace('Campaign name','')            
            cp_name=cp_name.strip()
        if 'Attempted sending' in i:
            cp_total=i.replace('Attempted sending','')            
            
        if 'Bad email addresses' in i:
            cp_bad=i.replace('Bad email addresses','')            
            
        if 'Successfully sent' in i:
            cp_good=i.replace('Successfully sent','')            
        
    #print cp_id+' - '+cp_name,int(cp_total),int(cp_bad),int(cp_good)
    a = sumarize(cp_name,int(cp_total),int(cp_bad),int(cp_good))
    return a
    
def main():
    infile = glob.glob( os.path.join(FILESPATH, '*.TXT') )
    for fil in infile:
        if 'LogFile' in fil: #and '20100826083051' in fil:
            #print fil
            data = read_file(fil)
            final = gather_data(data)
    claves = sortedDictValues2(final)
    sp=' '
    mx=38
    decimal.getcontext().prec=3
    print "*"*80
    print "Nombre de la Campaña"+sp*(mx-len("Nombre de la Campaña"))+"   Total"+"    Malos"+"   Enviados"+"  Pct Malos"
    print "*"*80
    for i in claves:
        #print i,final[i]        
        if final[i][1] == 0 or final[i][2] == 0:
            pct=0
        else:
            pct=(decimal.Decimal(final[i][1])/decimal.Decimal(final[i][0]))*100
            #print pct
        print i+sp*(mx-len(i))+str(final[i][0]).rjust(7)+str(final[i][1]).rjust(9)+str(final[i][2]).rjust(11)+str(pct).rjust(8)+"%"
        
            
main()
