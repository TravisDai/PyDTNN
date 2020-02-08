from NN_model import *
from NN_layer import *

def create_inceptionv3(comm, tracing):
    model = Model(comm, tracing)
    model.add( Input(shape=(225, 225, 3)) )
    model.add( Conv2D(nfilters=32, filter_shape=(3, 3, 3), padding=0, stride=2, activation="relu") )
    model.add( Conv2D(nfilters=32, filter_shape=(3, 3, 32), padding=1, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=64, filter_shape=(3, 3, 32), padding=1, stride=1, activation="relu") )
    model.add( Pool2D(pool_shape=(3,3), func='max', stride=2) )     #¿?¿?¿?¿?¿?
    model.add( Conv2D(nfilters=80, filter_shape=(1, 1, 64), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=192, filter_shape=(3, 3, 80), padding=1, stride=1, activation="relu") )
    model.add( Pool2D(pool_shape=(3,3), func='max', stride=2) )     #¿?¿?¿?¿?¿?
    model.add( Conv2D(nfilters=64, filter_shape=(1, 1, 192), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=48, filter_shape=(1, 1, 64), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=64, filter_shape=(5, 5, 48), padding=2, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=64, filter_shape=(1, 1, 64), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=96, filter_shape=(3, 3, 64), padding=1, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=96, filter_shape=(3, 3, 96), padding=1, stride=1, activation="relu") )
    model.add( Pool2D(pool_shape=(3,3), func='avg', stride=1) )     #PADDING=1
    model.add( Conv2D(nfilters=32, filter_shape=(1, 1, 96), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=64, filter_shape=(1, 1, 32), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=48, filter_shape=(5, 5, 64), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=64, filter_shape=(1, 1, 48), padding=2, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=64, filter_shape=(3, 3, 64), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=96, filter_shape=(3, 3, 64), padding=1, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=96, filter_shape=(3, 3, 96), padding=1, stride=1, activation="relu") )
    model.add( Pool2D(pool_shape=(3,3), func='avg', stride=1) )     #PADDING=1
    model.add( Conv2D(nfilters=64, filter_shape=(1, 1, 96), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=64, filter_shape=(1, 1, 64), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=48, filter_shape=(1, 1, 64), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=64, filter_shape=(5, 5, 48), padding=2, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=64, filter_shape=(1, 1, 64), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=96, filter_shape=(3, 3, 64), padding=1, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=96, filter_shape=(3, 3, 96), padding=1, stride=1, activation="relu") )
    model.add( Pool2D(pool_shape=(3,3), func='avg', stride=1) )     #PADDING=1
    model.add( Conv2D(nfilters=64, filter_shape=(1, 1, 96), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=384, filter_shape=(3, 3, 64), padding=0, stride=2, activation="relu") )      #¿?¿?¿?¿?¿? 
    model.add( Conv2D(nfilters=64, filter_shape=(1, 1, 384), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=96, filter_shape=(3, 3, 64), padding=1, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=96, filter_shape=(3, 3, 96), padding=0, stride=2, activation="relu") )     #¿?¿?¿?¿?¿?
    model.add( Pool2D(pool_shape=(3,3), func='max', stride=2) ) 
    model.add( Conv2D(nfilters=192, filter_shape=(1, 1, 96), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=128, filter_shape=(1, 1, 192), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=128, filter_shape=(1, 7, 128), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=192, filter_shape=(7, 1, 128), padding=3, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=128, filter_shape=(1, 1, 192), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=128, filter_shape=(7, 1, 128), padding=3, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=128, filter_shape=(1, 7, 128), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=128, filter_shape=(7, 1, 128), padding=3, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=192, filter_shape=(1, 7, 128), padding=0, stride=1, activation="relu") )
    model.add( Pool2D(pool_shape=(3,3), func='avg', stride=1) )     #PADDING=1
    model.add( Conv2D(nfilters=192, filter_shape=(1, 1, 192), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=192, filter_shape=(1, 1, 192), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=160, filter_shape=(1, 1, 192), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=160, filter_shape=(1, 7, 160), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=192, filter_shape=(7, 1, 160), padding=3, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=160, filter_shape=(1, 1, 192), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=160, filter_shape=(7, 1, 160), padding=3, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=160, filter_shape=(1, 7, 160), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=160, filter_shape=(7, 1, 160), padding=3, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=192, filter_shape=(1, 7, 160), padding=0, stride=1, activation="relu") )
    model.add( Pool2D(pool_shape=(3,3), func='avg', stride=1) )     #PADDING=1
    model.add( Conv2D(nfilters=192, filter_shape=(1, 1, 192), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=192, filter_shape=(1, 1, 192), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=192, filter_shape=(1, 1, 192), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=192, filter_shape=(1, 7, 192), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=192, filter_shape=(7, 1, 192), padding=3, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=192, filter_shape=(1, 1, 192), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=192, filter_shape=(7, 1, 192), padding=3, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=192, filter_shape=(1, 7, 192), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=192, filter_shape=(7, 1, 192), padding=3, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=192, filter_shape=(1, 7, 192), padding=0, stride=1, activation="relu") )
    model.add( Pool2D(pool_shape=(3,3), func='avg', stride=1) )     #PADDING=1
    model.add( Conv2D(nfilters=192, filter_shape=(1, 1, 192), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=192, filter_shape=(1, 1, 192), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=320, filter_shape=(3, 3, 192), padding=1, stride=2, activation="relu") )
    model.add( Conv2D(nfilters=192, filter_shape=(1, 1, 320), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=192, filter_shape=(1, 7, 192), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=192, filter_shape=(7, 1, 192), padding=3, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=192, filter_shape=(3, 3, 192), padding=0, stride=2, activation="relu") )
    model.add( Pool2D(pool_shape=(3,3), func='max', stride=2) )     #PADDING=1
    model.add( Conv2D(nfilters=320, filter_shape=(1, 1, 192), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=384, filter_shape=(1, 1, 320), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=384, filter_shape=(1, 3, 384), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=384, filter_shape=(3, 1, 384), padding=1, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=448, filter_shape=(1, 1, 384), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=384, filter_shape=(3, 3, 448), padding=1, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=384, filter_shape=(1, 3, 384), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=384, filter_shape=(3, 1, 384), padding=1, stride=1, activation="relu") )
    model.add( Pool2D(pool_shape=(3,3), func='avg', stride=1) )     #PADDING=1
    model.add( Conv2D(nfilters=192, filter_shape=(1, 1, 384), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=320, filter_shape=(1, 1, 192), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=384, filter_shape=(1, 1, 320), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=384, filter_shape=(1, 3, 384), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=384, filter_shape=(3, 1, 384), padding=1, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=448, filter_shape=(1, 1, 384), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=384, filter_shape=(3, 3, 448), padding=1, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=384, filter_shape=(1, 3, 384), padding=0, stride=1, activation="relu") )
    model.add( Conv2D(nfilters=384, filter_shape=(3, 1, 384), padding=1, stride=1, activation="relu") )
    model.add( Pool2D(pool_shape=(3,3), func='max', stride=1) )     #PADDING=1
    model.add( Conv2D(nfilters=192, filter_shape=(1, 1, 384), padding=0, stride=1, activation="relu") )
    model.add( Pool2D(pool_shape=(8,8), func='avg', stride=1) )     #PADDING!!
    model.add( Flatten() )
    model.add( FC(shape=(1000,), activation="sigmoid") )
    return model
