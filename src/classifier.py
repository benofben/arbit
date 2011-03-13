# Rebuild the training (and testing) points
#import arbit.predictors
#arbit.predictors.rebuild()

import arbit.classifier
classifier = arbit.classifier.classifier()

# now we want to run simulate on the classification table
import arbit.simulate
simluate = arbit.simulate.simulate()