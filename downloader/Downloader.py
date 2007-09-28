def download():
    # first we're going to delete all the old data
    import os
    import shutil
    if os.path.exists("data"):
        shutil.rmtree("data")

    import GetSymbols
    GetSymbols.getSymbols()

    import GetQuotes
    GetQuotes.processSymbolFile()
    
    import ReformatQuotes
    ReformatQuotes.ReformatQuoteFiles()

    import CreateTrainingAndTestingSets
    CreateTrainingAndTestingSets.CreateTrainingAndTestingSets()
