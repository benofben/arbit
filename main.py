"""
# download all the stock data
import downloader.Downloader
downloader.Downloader.download()

# compute beta using Matlab
import os
os.system("matlab -r computeBeta;exit")
"""

symbol=''

# run preprocessor for weka
import wekaPreprocessor.WekaTrainTestSets
wekaPreprocessor.WekaTrainTestSets.CreateTrainingSetForWeka()

# call weka
import downloader.ReformatQuotes
import os
symbols=downloader.ReformatQuotes.GetSymbols('data/train')

os.system("java -cp ./weka.jar weka.core.converters.CSVLoader data/weka/train" + symbol + ".csv > data/weka/train" + symbol + ".arff")
os.system("java -cp ./weka.jar weka.core.converters.CSVLoader data/weka/test" + symbol + ".csv > data/weka/test" + symbol + ".arff")
#os.system("java -cp ./weka.jar -Xmx1024M weka.classifiers.bayes.NaiveBayes -t data/weka/train" + symbol + ".arff > data/weka/" + symbol + "Out.txt")
#os.system("java -cp ./weka.jar -Xmx1024M weka.classifiers.bayes.NaiveBayes -t data/weka/train" + symbol + ".arff -T data/weka/test" + symbol + ".arff -p 0 > data/weka/" + symbol + "Out.txt")

# run post processor
#import wekaPostprocessor.toMatlab
#wekaPostprocessor.toMatlab.toMatlab(symbol)

# probably want to invoke Matlab and make some pretty graphs here
