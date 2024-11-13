import csv

def read_csv_to_list(filename):
    data_list = []
    
    with open(filename, mode='r', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)

        header = next(csvreader, None)
        
        for row in csvreader:
            data_list.append(row)
    
    return data_list


filename = './tesing.csv' 
# filename = './Final project//testing.csv'  
samples = read_csv_to_list(filename)
# print(samples)
samples = [sample[1] for sample in samples]
print(samples)