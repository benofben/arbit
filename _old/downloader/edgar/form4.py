import edgar.xmltodict
import os


def parse(filename):
    if not os.path.exists(filename):
        print('File does not exist!')
        return []

    if os.path.getsize(filename) == 0:
        print('File size is 0!')
        return []

    file = open(filename)

    for line in file:
        if line.startswith('<SEC-DOCUMENT>'):
            secDocument = line.replace('<SEC-DOCUMENT>', '')
            secDocument = secDocument.strip()
            break

    for line in file:
        if line.startswith('<ACCEPTANCE-DATETIME>'):
            acceptanceDatetime = line.replace('<ACCEPTANCE-DATETIME>', '')
            acceptanceDatetime = acceptanceDatetime.strip()
            break

    for line in file:
        if line.startswith('<?xml version="1.0"?>'):
            break

    contents = file.read()
    file.close()

    # need to delete everything after: </ownershipDocument>
    seperator = '</XML>'
    contents = contents.split(seperator, 1)[0]

    ownershipDocument = edgar.xmltodict.xmltodict(contents)

    issuerTradingSymbol = ownershipDocument['issuer'][0]['issuerTradingSymbol'][0]
    rptOwnerCik = ownershipDocument['reportingOwner'][0]['reportingOwnerId'][0]['rptOwnerCik'][0]
    rptOwnerName = ownershipDocument['reportingOwner'][0]['reportingOwnerId'][0]['rptOwnerName'][0]

    try:
        isDirector = ownershipDocument['reportingOwner'][0]['reportingOwnerRelationship'][0]['isDirector'][0]
        isDirector = convertTo01(isDirector)
    except KeyError:
        isDirector = False

    try:
        isOfficer = ownershipDocument['reportingOwner'][0]['reportingOwnerRelationship'][0]['isOfficer'][0]
        isOfficer = convertTo01(isOfficer)
    except KeyError:
        isOfficer = False

    try:
        isTenPercentOwner = \
        ownershipDocument['reportingOwner'][0]['reportingOwnerRelationship'][0]['isTenPercentOwner'][0]
        isTenPercentOwner = convertTo01(isTenPercentOwner)
    except KeyError:
        isTenPercentOwner = False

    try:
        isOther = ownershipDocument['reportingOwner'][0]['reportingOwnerRelationship'][0]['isOther'][0]
        isOther = convertTo01(isOther)
    except KeyError:
        isOther = False

    try:
        ownershipDocuments = ownershipDocument['nonDerivativeTable'][0]['nonDerivativeTransaction']
    except KeyError:
        return []
    except TypeError:
        return []

    transactions = []
    i = 0
    for nonDerivativeTransaction in ownershipDocuments:
        try:
            transactionDate = nonDerivativeTransaction['transactionDate'][0]['value'][0]
            transactionShares = nonDerivativeTransaction['transactionAmounts'][0]['transactionShares'][0]['value'][0]
            transactionPricePerShare = \
            nonDerivativeTransaction['transactionAmounts'][0]['transactionPricePerShare'][0]['value'][0]
            transactionAcquiredDisposedCode = \
            nonDerivativeTransaction['transactionAmounts'][0]['transactionAcquiredDisposedCode'][0]['value'][0]
            sharesOwned = \
            nonDerivativeTransaction['postTransactionAmounts'][0]['sharesOwnedFollowingTransaction'][0]['value'][0]

            if float(transactionPricePerShare) == 0:
                pass
            else:
                transaction = {}
                transaction['secDocument'] = secDocument + ' ' + str(i)
                i += 1

                transaction['acceptanceDatetime'] = acceptanceDatetime
                transaction['issuerTradingSymbol'] = issuerTradingSymbol
                transaction['rptOwnerCik'] = rptOwnerCik
                transaction['rptOwnerName'] = rptOwnerName
                transaction['isDirector'] = isDirector
                transaction['isOfficer'] = isOfficer
                transaction['isTenPercentOwner'] = isTenPercentOwner
                transaction['isOther'] = isOther
                transaction['transactionDate'] = transactionDate
                transaction['transactionShares'] = float(transactionShares)
                transaction['transactionPricePerShare'] = float(transactionPricePerShare)
                transaction['transactionAcquiredDisposedCode'] = transactionAcquiredDisposedCode
                transaction['sharesOwned'] = float(sharesOwned)
                transactions.append(transaction)

        except KeyError:
            pass

    return transactions


def convertTo01(s):
    if s == '0':
        return False
    elif s == '1':
        return True
    if s == 'false':
        return False
    elif s == 'true':
        return True
    else:
        print('Cannot figure out correct value.')
