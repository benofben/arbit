def run():
	npiFilename = 'C:/Users/ben/Desktop/Essilor/NPPES_Data_Dissemination_March_2011/npidata_20050523-20110314.csv'
	shivaFilename = 'C:/Users/ben/Desktop/Essilor/shiva_output_lastname2_addr_address1_Final.csv'
	npiMatchFilename = 'C:/Users/ben/Desktop/Essilor/npiMatch.csv'
	
	# read the shiva file into memory since it's smaller
	shivaFile = open(shivaFilename, 'r')
	lineNumber = 0
	LAST_NAME2 = []
	for line in shivaFile:
		if lineNumber != 0:
			# we need LAST_NAME2 which is column 6 (0 indexed)
			columns = line.split(',')
			LAST_NAME2.append(columns[6].replace('"',''))
		lineNumber+=1
	shivaFile.close()
	
	# now compare each LAST_NAME2 from the shiva file to called Provider Organization Name (Legal Business Name) in the NPI File
	# the column we want is number 4 (0 indexed)
	npiMatchFile = open(npiMatchFilename, 'w')
	npiMatchFile.close()
	
	npiFile = open(npiFilename, 'r')
	lineNumber = 0
	for line in npiFile:
		columns = line.split(',')
		ProviderOrganizationName = columns[4].replace('"','')
				
		for x in LAST_NAME2:		
			if x == ProviderOrganizationName:
				
				# check if all whitespace (and ignore if so)
				if len(x.lstrip())>0:
					print('Matched on ' + ProviderOrganizationName)
					npiMatchFile = open(npiMatchFilename, 'a')
					npiMatchFile.write(line)
					npiMatchFile.close()
					break

		lineNumber+=1
	npiFile.close()
	
	
run()