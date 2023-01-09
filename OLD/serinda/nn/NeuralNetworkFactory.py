# this factory takes whatever pretrained model we need to load or whatever NN is wanted to be used
from serinda.constants.NNConstants import NNConstants

# the idea is that you can say "use mnist" and it will load whatever NN is pretrained for it or coded already
#    or you can say "use tensorflow and load mnist" and if both pytorch and tensorflow are already set up then it'll use tensorflow
class NeuralNetworkFactory:
    def factory(self, pretrainedmodel):
        # look up pretrained model and then return the neural network
        # Keras, Tensorflow, PyTorch
        # Kaggle, Darknet
        # https://pypi.org/project/darknetpy/
        if pretrainedmodel == NNConstants.MNIST:
            
        else:
            return ""

