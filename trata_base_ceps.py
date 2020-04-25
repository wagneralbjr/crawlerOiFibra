import csv

with open('statewide.csv') as csvfile:
    spamreader = csv.reader(csvfile, delimiter= ',')
    #LON,LAT,NUMBER,STREET,UNIT,CITY,DISTRICT,REGION,POSTCODE,ID,HASH
    teste = [ [ x[0],x[1], x[8]] for x in spamreader ]

    ceps_inseridos = set()

    data_final = []
    for row in teste:
        if row[2] in ceps_inseridos:
            pass
        else:
            data_final.append(row)
            ceps_inseridos.add(row[2])    


with open('ceps_tratados.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                         quoting=csv.QUOTE_MINIMAL)
    
    #spamwriter.writerow(['LON','LAT','POSTCODE'])
    for row in data_final:
        spamwriter.writerow(row)
